import os
from threading import Thread
from multiprocessing import Process

import cv2
import numpy as np


def resize_video(source: str, target: str, size: tuple, dst_fps=10):
    cap = cv2.VideoCapture(source)

    orig_fps = int(cap.get(cv2.CAP_PROP_FPS))
    reduce_rate = dst_fps / orig_fps

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    # print(fps, width, height)

    writer = cv2.VideoWriter(target, fourcc, dst_fps, size)

    ret = True
    frame_cnt = 0
    while cap.isOpened() and ret:
        ret, frame = cap.read()
        frame_cnt += reduce_rate

        if ret and frame_cnt >= 1:
            frame = cv2.resize(frame, size)
            writer.write(frame)
            frame_cnt = 0
    cap.release()
    writer.release()


def batch_resize(video_paths: list, dst_path: str, dst_size: tuple):
    for i, v in enumerate(video_paths):
        print(i)
        basename = os.path.basename(v)
        resize_video(v, os.path.join(dst_path, basename), dst_size)
    print('completed.')


def distribute(path, dst_path, num_thread=5):
    # sub_dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]
    sub_dirs = [path]
    videos = []
    for sub_dir in sub_dirs:
        video_paths = [os.path.join(sub_dir, x) for x in os.listdir(sub_dir) if x.endswith('.avi')]
        videos.extend(video_paths)

    threads = []
    num_segment = int(len(videos) / num_thread)
    print('number of segment:', num_segment)
    for i in range(num_thread):
        start = i * num_segment
        if i != num_thread - 1:
            end = (i + 1) * num_segment
        else:
            end = len(videos) - 1

        th = Thread(target=batch_resize, args=(videos[start:end], dst_path, (320, 240)))
        threads.append(th)

    for th in threads:
        th.start()
    for i, th in enumerate(threads):
        th.join()
        print('thread', i, 'ok.')


if __name__ == '__main__':
    p1 = Process(target=distribute('/data/datasets/Robam/compressed_videos/val/grab',
                                   '/data/datasets/Robam/compressed_videos/val/grab1'))

    p2 = Process(target=distribute('/data/datasets/Robam/compressed_videos/val/other',
                                   '/data/datasets/Robam/compressed_videos/val/other1'))

    p1.start()
    p2.start()

