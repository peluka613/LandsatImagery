#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 13:43:34 2019

@author: peluka
"""


#import numpy as np
import matplotlib.pyplot as plt

import tifffile as tiff
plt.figure() 

im1 = tiff.imread('170323.tif')
im1 = im1[1:4,:,:]

im2 = tiff.imread('170324.tif')
im2 = im2[1:4,:,:]

im3 = tiff.imread('170614.tif')
im3 = im3[1:4,:,:]

im4 = tiff.imread('171224.tif')
im4 = im4[1:4,:,:]

im5 = tiff.imread('180615.tif')
im5 = im5[1:4,:,:]

tiff.imshow(im1)
plt.axis("off")

tiff.imshow(im2)
plt.axis("off")

tiff.imshow(im3)
plt.axis("off")

tiff.imshow(im4)
plt.axis("off")

tiff.imshow(im5)
plt.axis("off")

#******************************


