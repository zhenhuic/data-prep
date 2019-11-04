import cv2
import numpy as np


def change_color(img_path: str):
    # red -> orange
    img = cv2.imread(img_path)

    mask = img[:, :, 2].copy()
    # print(np.unique(mask, return_counts=True))

    img[mask >= 150] = [0, 80, 255]
    img[mask < 150] = [0, 0, 0]
    print(np.unique(img, return_counts=True))
    return img


if __name__ == '__main__':
    src = 'E:\\Lab417\\xio-intrusion-detection\\images\\masks\\baobantongyong.jpg'
    img = change_color(src)
    cv2.imshow('img', img)
    if cv2.waitKey(0) & 0xFF == ord('y'):
        cv2.imwrite(src, img)
        print('save')
    else:
        print('quit')
