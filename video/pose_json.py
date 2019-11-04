import json
import os
import random
import shutil

from tqdm import tqdm


def extract_openpose(json_file: str) -> list:
    with open(json_file, 'r') as f:
        data = json.load(f)

    for i in range(len(data)):
        key = '{}.jpg'.format(i)
        try:
            frame = data[key]
        except KeyError:
            continue
        people = frame['people']
        yield people


def coord_norm(x: float, y: float, score: float, img_shape: tuple) \
        -> (float, float, float):
    width, height = img_shape[0], img_shape[1]
    x = round(x / width, 3)
    y = round(y / width, 3)
    score = round(score, 3)
    return x, y, score


def convert_skeleton(openpose_people: list, num_person: int) -> (list, list):
    if len(openpose_people) == 1:
        openpose_people.append({"pose_keypoints_2d": [0.0] * 54})
    for i, person in enumerate(openpose_people):
        if i > num_person - 1:
            break
        keypoints = person['pose_keypoints_2d']
        pose = []
        score = []
        for idx, x in enumerate(keypoints[::3]):
            idx = idx * 3
            x, y, conf = coord_norm(x, keypoints[idx + 1],
                                    keypoints[idx + 2], (1280, 720))
            pose.extend([x, y])
            score.append(conf)

        yield pose, score


def kinetics_format(json_file: str, label: str, outdir: str):
    data = []
    for i, people in enumerate(extract_openpose(json_file)):
        frame = {"frame_index": i + 1, "skeleton": []}
        for pose, score in convert_skeleton(people, 2):
            frame["skeleton"].append({"pose": pose, "score": score})
        data.append(frame)

    label_index = len(data)

    video = {
        'data': data,
        'label': label,
        'label_index': label_index,
    }

    splits = json_file.split('/')
    filename = label + '_' + splits[-3] + '_' + splits[-2] + '.json'
    filename = os.path.join(outdir, filename)

    with open(filename, 'w') as f:
        json.dump(video, f)

    return video


def seg_train_val(datadir: str, outdir: str, ratio: float = 0.8):
    for file in tqdm(os.listdir(datadir), desc=datadir):
        src = os.path.join(datadir, file)
        if random.random() < ratio:
            target = os.path.join(outdir, 'train', file)
            shutil.copyfile(src, target)
        else:
            target = os.path.join(outdir, 'val', file)
            shutil.copyfile(src, target)


def gen_label_json(datadir: str):
    for phase in ['train', 'val']:
        path = os.path.join(datadir, phase)
        label_json = {}
        for example in tqdm(os.listdir(path), desc=phase):
            name = example.split('.')[0]
            with open(os.path.join(path, example), 'r') as f:
                data = json.load(f)
            label = data['label']
            label_index = data['label_index']
            label_json[name] = {"has_skeleton": True, "label": label, "label_index": label_index}
        with open(os.path.join(datadir, 'robam_{}_label.json'.format(phase)), 'w') as f:
            json.dump(label_json, f)


def main():
    path = '/data/datasets/Robam/AlphaPose_output/other/v_3'
    label = 'other'
    for d in tqdm(os.listdir(path)):
        json_file = os.path.join(path, d, 'alphapose-results.json')
        if os.path.exists(json_file):
            outdir = '/data/datasets/Robam/kinetics_format/' + label
            kinetics_format(json_file, label, outdir)


if __name__ == '__main__':
    # main()  # convert to kinetics format json
    # seg_train_val('E:/Datasets/Robam/kinetics_format/grab', 'E:/Datasets/Robam/robam-skeleton')
    gen_label_json('E:/Datasets/Robam/robam-skeleton')


