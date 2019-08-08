# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 18:58:56 2018

@author: FD
"""

import tensorflow as tf
import numpy as np

# use numpy generate data(phony data), total:100
x_data = np.float32(np.random.rand(2, 100))
y_data = np.dot([0.100, 0.200], x_data) + 0.300

# creat a liner model
b = tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0))
y = tf.matmul(W, x_data) + b

# minimize the variance
loss = tf.reduce_mean(tf.square(y - y_data))
train = tf.train.GradientDescentOptimizer(0.5).minimize(loss)

# initalization
init = tf.initialize_all_variables()

# graph
sess = tf.Session()
sess.run(init)

# fit the surface
for step in range(20000):
    sess.run(train)
    if step % 200 == 0:
        print ("step", sess.run(W), sess.run(b))










