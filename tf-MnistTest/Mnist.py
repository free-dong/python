# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 20:48:13 2018

@author: FD
"""

import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

sess = tf.InteractiveSession()
x = tf.placeholder("float", shape=[None, 784])
y_ = tf.placeholder("float", shape=[None, 10])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
sess.run(tf.initialize_all_variables())
y = tf.nn.softmax(tf.add(tf.matmul(x, W), b))
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
for i in range(1000):
    batch = mnist.train.next_batch(50)
    train_step.run(feed_dict = {x:batch[0], y_:batch[1]})
    if i%100 == 0:
        print("The %sst iter"%i)
        print(sess.run(accuracy,feed_dict = {x:batch[0], y_:batch[1]}))
#print(sess.run(accuracy,feed_dict = {x:mnist.test.images, y_:mnist.test.labels}))







