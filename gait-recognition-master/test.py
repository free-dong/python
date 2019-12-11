# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:21:13 2019

@author: feidong
步态检测：
测试所有的视频，每个视频生成一个向量
"""

import glob
import numpy as np
import json

from utils import read_video2array
from gait_nn import GaitNetwork
from human_pose_nn import HumanPoseIRNetwork

# read video
video_name_list = glob.glob(r'data/testa/050*.avi')

#gait recognition
net_pose = HumanPoseIRNetwork()
net_gait = GaitNetwork(recurrent_unit = 'GRU', rnn_layers = 2)
net_pose.restore(r'models/MPII+LSP.ckpt')
net_gait.restore(r'models/H3.6m-GRU-1.ckpt')

frames_label = []
identification = []
for index,item in enumerate(video_name_list):
    print("processing: %d/%d, %s" %(index, len(video_name_list), item))
    # labels for frame 
    person_id = item[11:14]
    path_name = item[11:24]
    frames_label.append(int(person_id))
    frames_arr = read_video2array(item, 2, path_name)
    # Create features from input frames in shape (TIME, HEIGHT, WIDTH, CHANNELS) 
    spatial_features = net_pose.feed_forward_features(frames_arr)
    # Process spatial features and generate identification vector 
    identification_vector, states = net_gait.feed_forward(spatial_features)
    #
    identification.append(np.array(identification_vector))

frames_label = np.array(frames_label)
video_name_list = np.array(video_name_list)
identification = np.array(identification)

# save id vector and label
np.save("output/frames_label.npy", frames_label) 
np.save("output/video_name_list.npy", video_name_list)
np.save("output/identification.npy", identification)
print('end---')

