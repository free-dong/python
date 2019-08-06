# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 15:11:26 2019

输入一个三维矩阵，设置合适大小的滤波器：
mode_filter：该滤波器可以根据众数对矩阵进行下采样。

@author: Free-Dong
"""

import numpy as np
import math

class filter:
    def __init__(self, input_matrix, filter_x=2, filter_y=2):
        # 设置滤波器的大小
        self.filter_x = filter_x
        self.filter_y = filter_y

        self.input_matrix = input_matrix
        
        # 读取输入图像、矩阵的大小
        [self.rows, self.columns, self.bands] = input_matrix.shape
        # 计算输出矩阵大小
        self.out_rows = math.ceil(self.rows/filter_x)
        self.out_columns = math.ceil(self.columns/filter_y)
        
    def mode_filter(self):
        # 初始化输出矩阵
        output_matrix = np.zeros([self.out_rows, self.out_columns, self.bands])
        
        out_i =0
        for i in range(0, self.rows-1, self.filter_x):
            out_j =0
            for j in range(0, self.columns-1, self.filter_y):
                
                filter_block = self.input_matrix[i:(i+self.filter_x), j:(j+self.filter_y), :]
                # bincount（）：统计非负整数的个数，不能统计浮点数
                counts = np.bincount(filter_block[:, :, 0].reshape(self.filter_x*self.filter_y).astype(int))
                # 返回众数
                mode_nb = np.argmax(counts)
                # 返回众数坐标
                [mode_x, mode_y] = np.where(filter_block[:, :, 0] == mode_nb)
                # 对output 赋值
                output_matrix[out_i, out_j, :] = filter_block[mode_x[0], mode_y[0], :]
                out_j=out_j+1
            out_i=out_i+1
        return output_matrix

a = np.linspace(1, 12*12*3, 12*12*3).reshape(12, 12, 3).astype(int)
b = np.ones([12, 13, 3])

a_filter = filter(input_matrix=a)
a_filter_mode = a_filter.mode_filter()

b_filter = filter(input_matrix=b)
b_filter_mode = b_filter.mode_filter()

import cv2
from PIL import Image

img=np.array(cv2.imread(r'D:\code\git\python\others\jump_demo\screen.png',cv2.IMREAD_COLOR)).astype(int)
img_filter = filter(input_matrix=img)
img_filter_mode = img_filter.mode_filter().astype(np.uint8)

import imageio
imageio.imwrite(r'D:\code\git\python\others\filter.jpg', img_filter_mode)

import matplotlib
matplotlib.image.imsave(r'D:\code\git\python\others\filter.jpg', img_filter_mode)
