# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:21:13 2019

@author: feido
"""

import glob
from scipy.misc import imresize, imread
import cv2
import numpy as np

from utils import read_video2array


video_name_list = glob.glob(r'data/test/*.avi')

frames_label = []
for index,item in enumerate(video_name_list):
    frames_arr = read_video2array(item, 1)
    # labels for frame 
    person_id = item[10:13]
    frames_label.append(int(person_id))
    
frames_label = np.array(frames_label)

print("frames_arr[0].shape: ", frames_arr.shape)
print("frames_label: ", frames_label)