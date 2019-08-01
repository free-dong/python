# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 10:26:13 2018
# =============================================================================
# LandMaskTime.py
# 陆地掩模：将遥感图像中的陆地掩盖掉，设置为0.
# 实验不同参数下陆地掩模运行时间
# =============================================================================
@author: feidong
"""

import numpy as np
import datetime
import h5py
import cv2
import os
import psutil
#import xlrd # 读取excel
import xlwt # 写入excel
#import matplotlib.pyplot as plt

def LandMaskProgram(blurKernel_num, fushiKernel_num, eroIte, dilIte, h5_num):
    # -------------------------------------------------------------------------
    # 工作路径
    workPath = "./data/"
    # 读取数据
    dataPath1 = workPath + "h5test-LandMaskProgram-" + h5_num + ".h5"
    #dataPath1 = workPath + "H1C_OPER_CZI_L1B_20190101T010500_00103_10.h5"
    #dataPath2 = workPath + "COMS_GOCI_L1B_GA_20160423001643_Area #1.he5"
    # 保存文件名
    h5fileSave = workPath + "temp/"
    if not os.path.exists(h5fileSave):
        os.makedirs(h5fileSave)
    h5fileTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    h5fileName = h5fileSave + "LandMask-" + str(h5fileTime) + ".h5"
    imgfileName = h5fileSave + "LandMask-" + str(h5fileTime) + ".jpg"
    file = h5py.File(dataPath1, "r")
    
    #band1 = file["HDFEOS/GRIDS/Image Data/Data Fields/Band 1 Image Pixel Values"][:]
    #读取遥感图像的绿波段和红波段
    # L 443--->blue;
    # L 565--->green;
    # L 665--->red;
    # L 685--->nir;
    
    band1 = file["Geophysical Data/L 443"][:]
    band2 = file["Geophysical Data/L 565"][:]
    band3 = file["Geophysical Data/L 665"][:]
    band4 = file["Geophysical Data/L 685"][:]
    [row,col] = band1.shape
    #band_number = 4
    #bands = np.zeros((row, col, band_number))
    #bands[:, :, 1] = band1
    
    # -------------------------------------------------------------------------
    # 计算NDWI
    # 进行NDWI运算
    band2_4 = np.array(band2 - band4)
    band24 = np.array(band2 + band4)
    NDWI_result = band2_4 / band24
    
    # -------------------------------------------------------------------------
    # 图像滤波
    #blurred = cv2.threshold(NDWI_result, 5, 0)
    blurKernel = (blurKernel_num, blurKernel_num)
    gaussianResult = cv2.GaussianBlur(NDWI_result, blurKernel, 1.5)
    
    # -------------------------------------------------------------------------
    # 腐蚀膨胀
    fushiKernel = (fushiKernel_num, fushiKernel_num)
    kernel = np.ones(fushiKernel, np.uint8)
    erosion = cv2.erode(gaussianResult, kernel, iterations = eroIte)
    dilation = cv2.dilate(erosion, kernel, iterations = dilIte)
    
    # -------------------------------------------------------------------------
    # 二值化
    # 设置阈值
    Threshold = 0.25
    ret,thresh = cv2.threshold(dilation, Threshold, 1, cv2.THRESH_BINARY)
    #plt.imshow(thresh)
    # -------------------------------------------------------------------------
    # 陆地掩模
    band1_landMask = band1 * thresh
    band2_landMask = band2 * thresh
    band3_landMask = band3 * thresh
    band4_landMask = band4 * thresh
    # -------------------------------------------------------------------------
    # 保存图像
    #plt.imshow(band1_landMask)  # 输出图像
    #plt.imshow(band1)
    writeData = h5py.File(h5fileName, "w")
    writeData["data/L 443"] = band1_landMask
    writeData["data/L 565"] = band2_landMask
    writeData["data/L 665"] = band3_landMask
    writeData["data/L 686"] = band4_landMask
    writeData.close()
    cv2.imwrite(imgfileName, band1_landMask)
    # -------------------------------------------------------------------------
    # 删除文件
    for i in os.listdir(h5fileSave):
        path_file = os.path.join(h5fileSave,i)  # 取文件路径
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            for f in os.listdir(path_file):  
                path_file2 =os.path.join(path_file,f)
                if os.path.isfile(path_file2):
                    os.remove(path_file2)

    return 0
 
# -----------------------------------------------------------------------------
# 测试函数
def test(blurKernel_num, fushiKernel_num, eroIte, dilIte):

    for i in range(100000):
        i += 1
    return 0
# =============================================================================
# 主程序:统计海陆掩模（LandMaskProgram）的不同输入参数的运行时间
# 设置输入参数列表
blurKernel_num_list = [1, 3, 5, 7]
fushiKernel_num_list = [1, 3, 5, 7]
eroIte_list = [1, 3, 5, 7, 9]
dilIte_list = [1, 3, 5, 7, 9]
h5_num = "3"   # 图像索引 
    
# blurKernel_num_list = [1, 3]
# fushiKernel_num_list = [1]
# eroIte_list = [1]
# dilIte_list = [1]

# 写入excel---------------------------------------------------------------------
# 创建workbook（excel）
fileTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
fileName =  "./data/result/LandMask-" + h5_num + "-" + str(fileTime) + ".xlsx"
workbook = xlwt.Workbook(encoding = 'ascii')
worksheet = workbook.add_sheet('fileTime') # 创建表

worksheet.write(0, 0, label = "Time") # 往单元格内写入内容Time
worksheet.write(0, 1, label = "fushiKernel_num")
worksheet.write(0, 2, label = "eroIte")
worksheet.write(0, 3, label = "dilIte")
worksheet.write(0, 4, label = "blurKernel_num")
worksheet.write(0, 5, label = "memory_total") 
worksheet.write(0, 6, label = "memory_free") 

Memoary_Hz = 1060   # 内存频率（MHz）
Memoary_cas = 15   # CAS延时（时钟）
cpu_Hz = 3.4   # cpu主频（MHz）
cpu_percent = psutil.cpu_percent(0)   # cpu使用率（%）
cpu_count = psutil.cpu_count()   # cpu核心数（个）
cpu_cache = 8   # cpu三级缓存（M）
disk_read = 200   # 磁盘读取传输速率（MB/s）
disk_write = 300   # 磁盘写入传输速率（MB/s）
dir_stor = 1.5308   # 文件大小（G）

worksheet.write(0, 7, label = "Memoary_Hz") # 往单元格内写入内容 Memoary_Hz
worksheet.write(0, 8, label = "Memoary_cas")
worksheet.write(0, 9, label = "cpu_Hz")
worksheet.write(0, 10, label = "cpu_percent")
worksheet.write(0, 11, label = "cpu_count")
worksheet.write(0, 12, label = "cpu_cache")
worksheet.write(0, 13, label = "disk_read")
worksheet.write(0, 14, label = "disk_write")
worksheet.write(0, 15, label = "dir_stor")

val_temp = 2**30   # 计算内存
# 运行LandMaskProgram
row = 1
for blurKernel_num in blurKernel_num_list:
    for fushiKernel_num in fushiKernel_num_list:
        for eroIte in eroIte_list:
            for dilIte in dilIte_list:
                info = psutil.virtual_memory()   # 返回内存使用情况
                memory_total = info.total/val_temp   # 总内存
                memory_free = info.free/val_temp   # free
                startTime = datetime.datetime.now() # 统计时间
                LandMaskProgram(blurKernel_num, fushiKernel_num, eroIte, dilIte, h5_num) # 运行测试程序
#                test(blurKernel_num, fushiKernel_num, eroIte, dilIte)
                endTime = datetime.datetime.now() # 统计时间
                runTime = str(endTime - startTime)
                
                worksheet.write(row, 0, label = runTime) # 往单元格内写入内容 runTime
                worksheet.write(row, 1, label = fushiKernel_num)
                worksheet.write(row, 2, label = eroIte)
                worksheet.write(row, 3, label = dilIte)
                worksheet.write(row, 4, label = blurKernel_num) 
                worksheet.write(row, 5, label = memory_total)
                worksheet.write(row, 6, label = memory_free)
                
                worksheet.write(row, 7, label = Memoary_Hz) # 往单元格内写入内容 Memoary_Hz
                worksheet.write(row, 8, label = Memoary_cas)
                worksheet.write(row, 9, label = cpu_Hz)
                worksheet.write(row, 10, label = cpu_percent)
                worksheet.write(row, 11, label = cpu_count)
                worksheet.write(row, 12, label = cpu_cache)
                worksheet.write(row, 13, label = disk_read)
                worksheet.write(row, 14, label = disk_write)
                worksheet.write(row, 15, label = dir_stor)
                print("row: ", row)
                row += 1

workbook.save(fileName) # 保存
print("end*******************************************************************")



