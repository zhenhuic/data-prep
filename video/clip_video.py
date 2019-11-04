import os
import time
from queue import Queue
from threading import Thread

import cv2
import numpy as np
import pandas as pd
from tqdm import tqdm


class VideoWriter:
    def __init__(self, path: str, video_info: dict):
        self.path = path
        self.info = video_info

        self.Q = Queue(maxsize=300)  # store frames to be writen
        self.writer = self._get_writer()

        self.stop = False

    def _get_writer(self) -> cv2.VideoWriter:
        writer = cv2.VideoWriter(self.path, self.info['fourcc'], self.info['fps'],
                                 (self.info['width'], self.info['height']))
        return writer

    def write(self, frame: np.array):
        self.Q.put(frame)

    def release(self):
        self.stop = True

    def start(self) -> Thread:
        th = Thread(target=self._update)
        th.daemon = True
        th.start()

        return th

    def _update(self):
        while True:
            if not self.Q.empty():
                frame = self.Q.get()
                self.writer.write(frame)
            elif self.stop:
                self.writer.release()
                break
            else:
                time.sleep(0.1)


def clip_video(cap: cv2.VideoCapture, slices: list, outdir: str) -> (cv2.VideoCapture, Thread):
    start, end = slices
    clip_name = '{}-{}.avi'.format(str(start), str(end))
    cap.set(cv2.CAP_PROP_POS_FRAMES, start)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    info = {'fps': fps, 'width': width, 'height': height,
            'fourcc': cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')}

    video_path = os.path.join(outdir, clip_name)

    writer = VideoWriter(video_path, info)
    thread = writer.start()

    for _ in range(start, end):
        ret, frame = cap.read()
        writer.write(frame)
    writer.release()

    return cap, thread


def strategy(length: int, exclude: np.array) -> np.array:
    video = np.ones(length, dtype=int)

    for e in exclude:
        middle = int((e[1] + e[0]) / 2)
        cnt = e[1] - e[0]

        cnt = int(0.6 * cnt)
        start, end = middle - cnt, middle + cnt
        video[start:end] = 0

    front, size = 0, 300  # sliding window, size 300
    rear = front + size
    stride = 100

    clips = []
    while rear < length:
        clip = video[front:rear]
        if np.sum(clip) == 300:
            clips.append([front, rear])
        elif np.sum(clip) >= 300 * 0.8:
            while video[front] != 1:
                front += 1
            while video[rear - 1] != 1:
                rear -= 1
            clip = video[front:rear]
            if np.unique(clip).size == 1:
                clips.append([front, rear])

        front += stride
        rear = front + size

    clips = np.array(clips, dtype=int)
    return clips


def main():
    video_path = 'E:\\Datasets\\Robam\\videos\\v_1.avi'
    grab_file = 'E:\\Datasets\\Robam\\videos\\grab\\v_1.txt'
    output_dir = 'E:\\Datasets\\Robam\\videos\\insignificance'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    cap = cv2.VideoCapture(video_path)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    grab_df = pd.read_csv(grab_file, sep=', ', engine='python')
    grab = grab_df[['start', 'end']].to_numpy()

    examples = strategy(count, grab)

    threads = []
    for example in tqdm(examples, desc='clip video'):
        start, end = example[0], example[1]
        cap, thread = clip_video(cap, [start, end], output_dir)
        threads.append(thread)

    for th in tqdm(threads, desc='write clips'):
        th.join()

    print('done')


if __name__ == '__main__':
    main()
