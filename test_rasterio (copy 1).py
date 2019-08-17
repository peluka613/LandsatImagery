#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 16:44:56 2019

@author: peluka
"""

import rasterio as rs
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np

import functions as fn

imgName1 = '170323'
im1 = rs.open(imgName1+ '.tif')

coastal1 = im1.read(1)
#plot.show(band1)

blue1 = im1.read(2).astype('float64')
#plot.show(blue1)

green1 = im1.read(3).astype('float64')
#plot.show(green1)

red1 = im1.read(4).astype('float64')
#plot.show(red1)

nir1 = im1.read(5).astype('float64')
#plot.show(nir1)

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
#plot.show(ndvi1)

ndvi1_img = rs.open(imgName1 +  'ndvi.tif', 'w', driver='Gtiff', dtype='float64', width=x, height=y, count=1,
                    crs=im1.crs, transform=im1.transform)
ndvi1_img.write(ndvi1, 1)
ndvi1_img.close()

_imgName1ndvi = rs.open(imgName1 +  'ndvi.tif')
#plot.show(_imgName1ndvi)

# ========================================================================
# MNDWI Water
mndwi1 = (green1 - swir11) / (green1 + swir11)
#plot.show(mndwi1)

mndwi1_img = rs.open(imgName1 +  'mndwi.tif', 'w', driver='Gtiff', dtype='float64', width=x, height=y, count=1,
                    crs=im1.crs, transform=im1.transform)
mndwi1_img.write(mndwi1, 1)
mndwi1_img.close()

_imgName1mndwi = rs.open(imgName1 +  'mndwi.tif')
#plot.show(_imgName1mndwi)

# ========================================================================

# UI Urban index
ui1 = (swir21 - nir1) / (swir21 + nir1)
#plot.show(ndvi1)

ui1_img = rs.open(imgName1 +  'ui1.tif', 'w', driver='Gtiff', dtype='float64', width=x, height=y, count=1,
                    crs=im1.crs, transform=im1.transform)
ui1_img.write(ui1, 1)
ui1_img.close()

_imgName1ui1 = rs.open(imgName1 +  'ui1.tif')
#plot.show(_imgName1ui1)

# ========================================================================


# ========================================================================
#   KMEANS
# ========================================================================

names1 = np.array(['ndvi1', 'mndwi1', 'ui1']) 
images1 = np.array([ndvi1, mndwi1, ui1])
#images1 = np.array([ndvi1])
N = 3
i = 2

#fn.myKMeansArray(images1, names1, N)
#fn.myKMeansArrayOnlyIt(images1, names1, N, i)

#fn.myKMeans(ndvi1, 'ndvi1', N)
ndvi1 = fn.my_inversa(fn.myKMeansByIt(ndvi1, N, i))
fn.print_gray_no_override_title(ndvi1, 'ndvi1 - ind ' + str(i))  

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



















