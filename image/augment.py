import os
import shutil
from tqdm import tqdm


def copyfile(path: str):
    files = [x for x in os.listdir(path) if x.endswith('.jpg')]
    for filename in tqdm(files):
        for i in range(10):
            new_filename = filename[:-4] + '_' + str(i + 1) + filename[-4:]
            shutil.copyfile(os.path.join(path, filename), os.path.join(path, new_filename))


if __name__ == '__main__':
    path = 'E:\\Datasets\\Robam\\local_crop\\carton_tube_other\\raw_data\\tube'
    copyfile(path)
