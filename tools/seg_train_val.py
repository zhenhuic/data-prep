import os
import shutil
import random
from tqdm import tqdm


if __name__ == '__main__':
    data_root = '/data/datasets/Robam/compressed_videos'
    ratio = 0.25
    raw_data = '/data/datasets/Robam/compressed_videos/other'
    files = [x for x in os.listdir(raw_data) if x.endswith('.avi')]

    for filename in tqdm(files):
        file = os.path.join(raw_data, filename)
        if random.random() < ratio:
            dst_path = os.path.join(data_root, 'val', os.path.basename(raw_data))
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            shutil.copyfile(file, os.path.join(dst_path, filename))
        else:
            dst_path = os.path.join(data_root, 'train', os.path.basename(raw_data))
            if not os.path.exists(dst_path):
                os.makedirs(dst_path)
            shutil.copyfile(file, os.path.join(dst_path, filename))
    print('ok')
