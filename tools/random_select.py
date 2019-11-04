import os
import shutil
import random
from tqdm import tqdm


def random_remove(path: str, dst_path: str):
    files = [x for x in os.listdir(path) if x.endswith('.avi')]

    for filename in tqdm(files, desc='random select'):
        if random.random() < 0.3:
            src = os.path.join(path, filename)
            dst = os.path.join(dst_path, filename)
            # os.remove(file)
            shutil.move(src, dst)


if __name__ == '__main__':
    path = '/data/datasets/Robam/compressed_videos/other'
    dst_path = '/data/datasets/Robam/compressed_videos/trash'
    random_remove(path, dst_path)
