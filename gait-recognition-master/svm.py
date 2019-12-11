# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:32:47 2019

@author: feido
"""

import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV

# read data
data = np.load("../output/identification.npy")
label = np.load("../output/frames_label.npy")
video_name_list = np.load("../output/video_name_list.npy")

# 划分数据与标签
train_data,test_data,train_label,test_label = train_test_split(
        data, label, random_state=1, test_size=0.3)

# 训练svm分类器
classifier=svm.SVC(C=9,kernel='linear',gamma=0.5,decision_function_shape='ovr') # ovr:一对多策略
classifier.fit(train_data,train_label.ravel()) #ravel函数在降维时默认是行序优先

# 计算svc分类器的准确率
print("训练集：", classifier.score(train_data, train_label))
print("测试集：", classifier.score(test_data, test_label))

result = classifier.predict(test_data[0:10])  # 使用模型预测值
print('预测结果：',result)  # 输出预测值[-1. -1.  1.  1.]

## rbf核函数，设置数据权重
#svc = svm.SVC(kernel='rbf', class_weight='balanced',)
#c_range = np.logspace(-5, 15, 11, base=2)
#gamma_range = np.logspace(-9, 3, 13, base=2)
## 网格搜索交叉验证的参数范围，cv=3,3折交叉
#param_grid = [{'kernel': ['rbf'], 'C': c_range, 'gamma': gamma_range}]
#grid = GridSearchCV(svc, param_grid, cv=3, n_jobs=-1)
## 训练模型
#clf = grid.fit(train_data, train_label)
## 计算测试集精度
#score = grid.score(test_data, test_label)
#print('精度为%s' % score)