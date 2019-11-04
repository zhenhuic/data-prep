import os
from tqdm import tqdm
import cv2


def record_length_videos(path):
    """
    Record length of clips to text file
    :param path: str, video path or directory of clips
    :param output: str, file path of output
    :return: tuple, (name, frame_count)
    """
    if path.endswith('.avi'):
        names = [path.split('.')[0]]
        root = ''
    else:

        names = [int(x.split('.')[0]) for x in os.listdir(path) if x.endswith('.avi')]
        names.sort()
        root = path

    for name in tqdm(names):
        cap = cv2.VideoCapture(root + str(name) + '.avi')
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        yield name, frame_count


def traverse_clips(path, output):
    with open(output, 'a') as f:
        f.write('start, end, count\n')
        for name, frame_count in record_length_videos(path):
            f.write('{}, {}, {}\n'.format(name, str(int(name) + int(frame_count)), str(frame_count)))
    print('OK')


if __name__ == '__main__':
    path = 'E:/Datasets/Robam/videos/grab/vlc-record-2019-08-29-14h26m42s/'
    output = 'E:/Datasets/Robam/videos/grab/vlc-record-2019-08-29-14h26m42s.txt'
    traverse_clips(path, output)
