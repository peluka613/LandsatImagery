#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 16:44:56 2019

@author: peluka
"""
import functions as fn

import rasterio as rs
from rasterio import plot
import numpy as np

import matplotlib.pyplot as plt
import cv2


imgName1 = '170323'
imgName2 = '170324'
imgName3 = '170614'
imgName4 = '171224'
imgName5 = '180615'

imgName = imgName1;
im1 = rs.open(imgName + '.tif')

coastal1 = im1.read(1).astype('float64')
blue1 = im1.read(2).astype('float64')
green1 = im1.read(3).astype('float64')
red1 = im1.read(4).astype('float64')
nir1 = im1.read(5).astype('float64')
swir11 = im1.read(6).astype('float64')
swir21 = im1.read(7).astype('float64')

y, x = blue1.shape
rgb = np.zeros(shape=(3,y,x))
rgb[0,:,:] = red1
rgb[1,:,:] = green1
rgb[2,:,:] = blue1

rgb = np.uint16(rgb / 256)
plot.show(rgb)

"""
ngb = np.zeros(shape=(3,y,x))
ngb[0,:,:] = nir1
ngb[1,:,:] = green1
ngb[2,:,:] = blue1

plot.show(np.uint16(ngb / 256))
"""

# ========================================================================

# NDVI Vegetación
ndvi1 = (nir1 - red1) / (nir1 + red1)
plot.show(ndvi1)

ndvi1_img = rs.open(imgName +  'ndvi.tif', 'w', driver='Gtiff', dtype='float64', width=x, height=y, count=1,
                    crs=im1.crs, transform=im1.transform)
ndvi1_img.write(ndvi1, 1)
ndvi1_img.close()

_imgName1ndvi = rs.open(imgName +  'ndvi.tif')
#plot.show(_imgName1ndvi)

# ========================================================================
# MNDWI Water
mndwi1 = (green1 - swir11) / (green1 + swir11)
plot.show(mndwi1)

mndwi1_img = rs.open(imgName +  'mndwi.tif', 'w', driver='Gtiff', dtype='float64', width=x, height=y, count=1,
                    crs=im1.crs, transform=im1.transform)
mndwi1_img.write(mndwi1, 1)
mndwi1_img.close()

_imgName1mndwi = rs.open(imgName +  'mndwi.tif')
#plot.show(_imgName1mndwi)

# ========================================================================

# UI Urban index
ui1 = (swir21 - nir1) / (swir21 + nir1)
plot.show(ndvi1)

ui1_img = rs.open(imgName +  'ui1.tif', 'w', driver='Gtiff', dtype='float64', width=x, height=y, count=1,
                    crs=im1.crs, transform=im1.transform)
ui1_img.write(ui1, 1)
ui1_img.close()

_imgName1ui1 = rs.open(imgName +  'ui1.tif')
#plot.show(_imgName1ui1)

# ========================================================================
# ========================================================================

plt.gray()

l = 0.3
ndvi1[ndvi1 < l] = 0
ndvi1[ndvi1 >= l] = 1
plot.show(ndvi1)

l = 0.08
mndwi1[mndwi1 < l] = 0
mndwi1[mndwi1 >= l] = 1
plot.show(mndwi1)

l = -0.1
ui1[ui1 > -0.1] = 1
ui1[ui1 <= -0.1] = 0
#plot.show(ui1)

ui = fn.binary_diference(ui1, mndwi1)
fn.print_gray_no_override_title(ui, 'ui') 

# ========================================================================
#   KMEANS
# ========================================================================
"""
names1 = np.array(['ndvi1', 'mndwi1', 'ui1']) 
images1 = np.array([ndvi1, mndwi1, ui1])
#images1 = np.array([ndvi1])
N = 3
i = 2

#fn.myKMeansArray(images1, names1, N)
#fn.myKMeansArrayOnlyIt(images1, names1, N, i)

#fn.myKMeans(ndvi1, 'ndvi1', N)
ndvi1 = fn.myKMeansByIt(ndvi1, N, i)
fn.print_gray_no_override_title(ndvi1, 'ndvi1 - ind ' + str(i))  

ndvi1Inv = fn.my_inversa(ndvi1)
fn.print_gray_no_override_title(ndvi1Inv, 'ndvi1Inv - ind ' + str(i))  

#fn.myKMeans(mndwi1, 'mndwi1', N)
mndwi1 = fn.myKMeansByIt(mndwi1, N, i)
fn.print_gray_no_override_title(mndwi1, 'mndwi1 - ind ' + str(i))  

N = 4
i = 2
#fn.myKMeans(ui1, 'ui1', N)
ui1 = fn.myKMeansByIt(ui1, N, i)
fn.print_gray_no_override_title(ui1, 'ui1 - ind ' + str(i))  

ui = fn.binary_diference(ui1, mndwi1)
fn.print_gray_no_override_title(ui, 'ui')  
"""
# ========================================================================
# CV2
# ========================================================================
"""
kernel = np.ones((3,3),np.uint8)
erosion =cv2.erode(ui, kernel, iterations = 1) 
dilation = cv2.dilate(ui, kernel, iterations = 1)
opening = cv2.morphologyEx(ui, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(ui, cv2.MORPH_CLOSE, kernel)

plt.figure()
plt.subplot(221)
plt.imshow(erosion,cmap='gray')
plt.subplot(222)
plt.imshow(dilation,cmap='gray')
plt.subplot(223)
plt.imshow(opening,cmap='gray')
plt.subplot(224)
plt.imshow(closing,cmap='gray')
"""

# ========================================================================
# ========================================================================

# ========================================================================
# GAMMA
# ========================================================================
"""
ar = np.array([0.05, 0.10, 0.20, 0.50, 1, 1.5, 2.5, 5.0, 10.0, 25.0])
#ar = np.array([0.10, 0.20, 0.50])

for x in range(ar.size):
    Im2 = fn.my_gamma(ndvi1, ar[x])
    title = 'ndvi1 = ' + str(ar[x])
    fn.print_gray_no_override_title(Im2, title)
    
for x in range(ar.size):
    Im2 = fn.my_gamma(mndwi1, ar[x])
    title = 'mndwi1 = ' + str(ar[x])
    fn.print_gray_no_override_title(Im2, title)

for x in range(ar.size):
    Im2 = fn.my_gamma(ui1, ar[x])
    title = 'ui1 = ' + str(ar[x])
    fn.print_gray_no_override_title(Im2, title)    
"""
# ========================================================================
# ========================================================================    



















