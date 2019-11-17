import os
from threading import Thread

import cv2
import numpy as np
from tqdm import tqdm


def video_optical_flow(video_path: str, save_dir: str):
    u_dir = os.path.join(save_dir, 'u')
    v_dir = os.path.join(save_dir, 'v')
    if not os.path.exists(u_dir):
        os.makedirs(u_dir)
    if not os.path.exists(v_dir):
        os.makedirs(v_dir)

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

    tvl1 = cv2.optflow.DualTVL1OpticalFlow_create()  # opencv 4.x
    # tvl1 = cv2.DualTVL1OpticalFlow_create()  # opencv 3.x

    ret = False
    front_frame = None
    while not ret:
        ret, front_frame = cap.read()
    front_gray = cv2.cvtColor(front_frame, cv2.COLOR_BGR2GRAY)

    pbar = tqdm(desc=os.path.basename(video_path), total=frame_count)
    while cap.isOpened() and ret:
        pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        ret, rear_frame = cap.read()
        if ret:
            pbar.update()

            rear_gray = cv2.cvtColor(rear_frame, cv2.COLOR_BGR2GRAY)

            flow = tvl1.calc(front_gray, rear_gray, None)

            front_gray = rear_gray

            flow[flow > 20] = 0
            flow[flow < -20] = 0

            flow = np.rint((flow + 20) / 20 * 127)
            flow = flow.astype(np.uint8)

            flow_u = np.zeros((240, 320, 1))
            flow_u = flow[..., 0]
            flow_v = np.zeros((240, 320, 1))
            flow_v = flow[..., 1]

            u_path = os.path.join(u_dir, str(pos) + '.jpg')
            v_path = os.path.join(v_dir, str(pos) + '.jpg')

            # cv2.imshow('u', flow_u)
            # cv2.imshow('v', flow_v)
            # cv2.waitKey(1)
            cv2.imwrite(u_path, flow_u)
            cv2.imwrite(v_path, flow_v)
    pbar.close()
    cap.release()


def batch_extract(video_dir: str, out_dir: str):
    video_names = [x for x in os.listdir(video_dir) if x.endswith('.avi')]
    print(video_dir, len(video_names), "videos:")

    for i, video in enumerate(video_names):
        print(i, 'th')
        flow_out_path = os.path.join(out_dir, video[:-4])
        if not os.path.exists(flow_out_path):
            os.makedirs(flow_out_path)

            video_path = os.path.join(video_dir, video)
            video_optical_flow(video_path, flow_out_path)


if __name__ == '__main__':
    # batch_extract('E:\\Datasets\\Robam\\compressed_videos\\train\\grab',
    #               'E:\\Datasets\\Robam\\flow\\train\\grab')

    # batch_extract('E:\\Datasets\\Robam\\compressed_videos\\train\\other',
    #               'E:\\Datasets\\Robam\\flow\\train\\other')
    #
    # batch_extract('E:\\Datasets\\Robam\\compressed_videos\\val\\grab',
    #               'E:\\Datasets\\Robam\\flow\\val\\grab')
    #
    batch_extract('E:\\Datasets\\Robam\\compressed_videos\\val\\other',
                  'E:\\Datasets\\Robam\\flow\\val\\other')
