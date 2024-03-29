import numpy as np

from functools import lru_cache
from scipy.stats import multivariate_normal

from scipy.misc import imresize, imread
import cv2

@lru_cache()
def get_gauss_pdf(sigma):
    n = sigma * 8

    x, y = np.mgrid[0:n, 0:n]
    pos = np.empty(x.shape + (2,))
    pos[:, :, 0] = x
    pos[:, :, 1] = y

    rv = multivariate_normal([n / 2, n / 2], [[sigma ** 2, 0], [0, sigma ** 2]])
    pdf = rv.pdf(pos)

    heatmap = pdf / np.max(pdf)

    return heatmap


def to_int(num):
    return int(round(num))


@lru_cache()
def get_binary_mask(diameter):
    d = diameter
    _map = np.zeros((d, d), dtype = np.float32)

    r = d / 2
    s = int(d / 2)

    y, x = np.ogrid[-s:d - s, -s:d - s]
    mask = x * x + y * y <= r * r

    _map[mask] = 1.0

    return _map


def get_binary_heat_map(shape, is_present, centers, diameter = 9):
    n = diameter
    r = int(n / 2)
    hn = int(2 * n)
    qn = int(4 * n)
    pl = np.zeros((shape[0], shape[1] + qn, shape[2] + qn, shape[3]), dtype = np.float32)

    for i in range(shape[0]):
        for j in range(shape[3]):
            my = centers[i, 0, j] - r
            mx = centers[i, 1, j] - r

            if -n < my < shape[1] and -n < mx < shape[2] and is_present[i, j]:
                pl[i, my + hn:my + 3 * n, mx + hn:mx + 3 * n, j] = get_binary_mask(diameter)

    return pl[:, hn:-hn, hn:-hn, :]


def get_gauss_heat_map(shape, is_present, mean, sigma = 5):
    n = to_int(sigma * 8)
    hn = to_int(n / 2)
    dn = int(2 * n)
    qn = int(4 * n)
    pl = np.zeros((shape[0], shape[1] + qn, shape[2] + qn, shape[3]), dtype = np.float32)

    for i in range(shape[0]):
        for j in range(shape[3]):
            my = mean[i, 0, j] - hn
            mx = mean[i, 1, j] - hn

            if -n < my < shape[1] and -n < mx < shape[2] and is_present[i, j]:
                pl[i, my + dn:my + 3 * n, mx + dn:mx + 3 * n, j] = get_gauss_pdf(sigma)
                # else:
                #     print(my, mx)

    return pl[:, dn:-dn, dn:-dn, :]

def read_video2array(path, timeFrame, path_name):
    vc = cv2.VideoCapture(path)  # 读入视频文件，命名cv
    n = 1  # 计数
     
    if vc.isOpened():  # 判断是否正常打开
        rval, frame = vc.read()
    else:
        rval = False
     
    timeF = timeFrame  # 视频帧计数间隔频率
     
    i = 0
    frames_arr = [] # 多帧
    while rval:  # 循环读取视频帧
        rval, frame = vc.read()
        if ((n % timeF == 0) and (n>10) and (n<80)):  # 每隔timeF帧进行存储操作
            i += 1
            #print(i)
            #cv2.imwrite('data/framesplit/{}.jpg'.format(i), frame)  # 存储为图像
            #cv2.imwrite('data/framesplit.jpg', frame)  # 存储为图像
            #frame = cv2.imread('data/framesplit.jpg')
            #print("frame: ", frame)
            if (i==30):
                save_path = 'data/framesplit/' + path_name + '.jpg'
                cv2.imwrite(save_path, frame)  # 存储为图像
            frame_arr = np.array(frame)
            if (frame_arr.shape):
                frame = cv2.resize(frame, (299, 299))
                frames_arr.append(frame)
        n = n + 1
        #cv2.waitKey(1)
    vc.release()
    frames_arr = np.array(frames_arr)
    return frames_arr