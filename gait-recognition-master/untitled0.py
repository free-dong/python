# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:48:48 2019

@author: feido
"""

import numpy as np

identification = np.load("output/MPII+LSP -- M+L-GRU-2-3000/identification.npy")
frames_label = np.load("output/MPII+LSP -- M+L-GRU-2-3000/frames_label.npy")
video_name_list = np.load("output/MPII+LSP -- M+L-GRU-2-3000/video_name_list.npy")

name = []
for index,item in enumerate(video_name_list):
    path_name = item[11:24] + '.jpg'
    name.append(path_name)
        
name = np.array(name)

# save id vector and label
np.save("./name.npy", name) 
    
# 第几个视频
id_vedio = 2198
# 计算余弦相似度
def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a 
    :param vector_b: 向量 b
    :return: sim
    """
    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    sim = 0.5 + 0.5 * cos
    return sim

results = []
for i in range(identification.shape[0]):
    result = cos_sim(identification[id_vedio], identification[i])
    results.append(result)
results_arr = np.array(results)

# 合并
results_2 = np.vstack([frames_label, results_arr])
results_2t = results_2.T
# sort
results_2t = results_2t * [1, -1]
results_sort = results_2t[np.argsort(results_2t[:,1])]

    

    
    
    
    