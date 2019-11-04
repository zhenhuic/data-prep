import argparse
import time
import os
import threading
import queue

import cv2


class VideoWriter:
    def __init__(self, queue, filename, info):
        self.queue = queue
        self.filename = filename
        self.info = info
        self.writer = self.get_writer()

        self.stop = False
        self.start()

    def get_writer(self):
        writer = cv2.VideoWriter(self.filename,
                                 cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                 self.info['fps'],
                                 (self.info['width'], self.info['height']))
        return writer

    def start(self):
        th = threading.Thread(target=self.update, args=())
        th.daemon = True
        th.start()

    def update(self):
        while True:
            if not self.queue.empty():
                frame = self.queue.get()
                self.writer.write(frame)
            elif self.queue.empty() and self.stop:
                self.writer.release()


def video_info(capture):
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # fps = capture.get(cv2.CAP_PROP_FPS)
    fps = 25
    frame_cnt = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    ret = {
        'width': width,
        'height': height,
        'fps': fps,
        'count': frame_cnt,
    }
    return ret


def main(args):
    video_path = args.video
    begin_frame = args.begin

    writer = None
    cap = cv2.VideoCapture(video_path)
    info = video_info(cap)
    print('视频信息:', info)

    if begin_frame > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, begin_frame)

    speed = 1
    origin = int(1 / info['fps'] * 1000)
    delay = origin

    name = video_path.split('/')[-1].split('.')[0]
    root = 'output/' + name + '/'
    if not os.path.exists(root):
        os.makedirs(root)

    while cap.isOpened():
        # capture frame-by-frame
        ret, frame = cap.read()

        if writer is not None:
            Q.put(frame)

        # display the resulting frame
        cv2.imshow('frame', frame)

        res = cv2.waitKey(delay)
        if res & 0xFF == ord('q'):
            break
        elif res & 0xFF == ord('s'):
            if writer is not None and not writer.stop:
                print('动作尚未设置终止帧')
            elif writer is not None and writer.stop and not Q.empty():
                while not Q.empty():
                    time.sleep(1)
                pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
                print('动作起始帧:', pos)
                Q = queue.Queue(maxsize=200)
                writer = VideoWriter(Q, root + str(pos) + '.avi', info)

                with open(root + name + '.txt', 'a') as f:
                    f.write(str(pos) + ', ')

            elif writer is None or writer.stop and Q.empty():
                pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
                print('动作起始帧:', pos)
                Q = queue.Queue(maxsize=200)
                writer = VideoWriter(Q, root + str(pos) + '.avi', info)

                with open(root + name + '.txt', 'a') as f:
                    f.write(str(pos) + ', ')

        elif res & 0xFF == ord('e'):
            if writer is None:
                print('动作尚未设置起始帧')
            else:
                pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
                print('动作终止帧:', pos)
                print()
                writer.stop = True

                with open(root + name + '.txt', 'a') as f:
                    f.write(str(pos) + '\n')

        elif res & 0xFF == ord('-'):
            if speed > 0.5:
                speed -= 0.5
                delay = int(origin / speed)
            print('倍速:', speed)
        elif res & 0xFF == ord('='):
            if speed < 5:
                speed += 0.5
                delay = int(origin / speed)
            print('倍速:', speed)
        elif res & 0xFF == ord('p'):
            cv2.waitKey(0)
        elif res & 0xFF == ord('j'):
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos - 25)
        elif res & 0xFF == ord('h'):
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos - 100)
        elif res & 0xFF == ord('k'):
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos + 25)
        elif res & 0xFF == ord('l'):
            pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            cap.set(cv2.CAP_PROP_POS_FRAMES, pos + 200)

    cap.release()
    if writer is not None:
        writer.stop = True
    cv2.destroyAllWindows()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", type=str,
                        default='E:/Datasets/Robam/videos/output_4.avi',
                        help="video path")
    parser.add_argument("-b", "--begin", type=int, default=0,
                        help="frame position of beginning display")

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    print(args)
    main(args)
