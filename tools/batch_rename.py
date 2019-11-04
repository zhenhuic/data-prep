import os
from tqdm import tqdm


def dst_name_template(src: str) -> str:
    assert os.path.isfile(src)

    dirname = os.path.dirname(src)
    basename = os.path.basename(src)

    dirs = dirname.split(os.sep)
    new_name = str(dirs[-2]) + '_' + str(dirs[-1]) + '_' + basename

    dst = os.path.join(dirname, new_name)
    return dst


def batch_rename(path: str):
    files = [os.path.join(path, x) for x in os.listdir(path)
             if os.path.isfile(os.path.join(path, x))]
    for file in files:
        dst = dst_name_template(file)
        os.rename(file, dst)


if __name__ == '__main__':
    # src = '/data/datasets/Robam/videos/grab/v_1/8.avi'
    path = '/data/datasets/Robam/videos/other/'
    dirs = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

    for p in tqdm(dirs, desc=path):
        batch_rename(p)

