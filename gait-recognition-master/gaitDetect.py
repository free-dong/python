import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.misc import imresize, imread
import cv2

from utils import read_video2array
from gait_nn import GaitNetwork
from human_pose_nn import HumanPoseIRNetwork
mpl.use('Agg')

#
net_pose = HumanPoseIRNetwork()
net_gait = GaitNetwork(recurrent_unit = 'GRU', rnn_layers = 2)
net_pose.restore('models/MPII+LSP.ckpt')
net_gait.restore('models/H3.6m-GRU-1.ckpt')

# read image data
# img = imread('images/dummy.jpg')
# img = imresize(img, [299, 299])
# img_batch = np.expand_dims(img, 0)

# read feames in shape (TIME, HEIGHT, WIDTH, CHANNELS)
frames_arr = read_video2array('data/test/062-nm-04-126.avi', 1)

# Create features from input frames in shape (TIME, HEIGHT, WIDTH, CHANNELS) 
spatial_features = net_pose.feed_forward_features(frames_arr)

# Process spatial features and generate identification vector 
identification_vector = net_gait.feed_forward(spatial_features)

print("identification_vector[0].shape: ", identification_vector[0].shape)
np.save("identification_vector.npy", identification_vector[0]) 

