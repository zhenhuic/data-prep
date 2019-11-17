import os

import cv2
from tqdm import tqdm


def extract_frame(video_path: str, save_dir: str):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1

    ret = True
    pbar = tqdm(desc=os.path.basename(video_path), total=frame_count)
    while cap.isOpened() and ret:
        pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        ret, frame = cap.read()
        if ret:
            pbar.update()
            frame_path = os.path.join(save_dir, str(pos) + '.jpg')
            cv2.imwrite(frame_path, frame)
    pbar.close()
    cap.release()


def batch_extract(video_dir: str, out_dir: str):
    video_names = [x for x in os.listdir(video_dir) if x.endswith('.avi')]
    print(video_dir, len(video_names), "videos:")

    for i, video in enumerate(video_names):
        print(i, 'th')
        frame_dir = os.path.join(out_dir, video[:-4])
        if not os.path.exists(frame_dir):
            os.makedirs(frame_dir)

            video_path = os.path.join(video_dir, video)
            extract_frame(video_path, frame_dir)


if __name__ == '__main__':
    batch_extract('E:\\Datasets\\Robam\\compressed_videos\\train\\grab',
                  'E:\\Datasets\\Robam\\extracted_frames\\train\\grab')

    batch_extract('E:\\Datasets\\Robam\\compressed_videos\\train\\other',
                  'E:\\Datasets\\Robam\\extracted_frames\\train\\other')

    batch_extract('E:\\Datasets\\Robam\\compressed_videos\\val\\grab',
                  'E:\\Datasets\\Robam\\extracted_frames\\val\\grab')
    #
    batch_extract('E:\\Datasets\\Robam\\compressed_videos\\val\\other',
                  'E:\\Datasets\\Robam\\extracted_frames\\val\\other')
