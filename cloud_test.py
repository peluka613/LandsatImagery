#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:59:34 2019

@author: peluka
"""

import functions as fn
import rasterio as rs
from rasterio import plot
import numpy as np

# Lista de imágenes a procesar
images = np.array(['170323.tif', '170324.tif', '170614.tif', '171224.tif', '180615.tif'])
#images = np.array(['170323.tif'])

# Arreglos para contener las imágenes procesadas
rgbs = [None] * len(images)
clouds = [None] * len(images)
clouds = [None] * len(images)
ndvi = [None] * len(images)
mndwi = [None] * len(images)
ui = [None] * len(images)

x = 0
y = 0

# Recorrer la lista de imágenes, procesarlas y agregarlas a los arreglos correspondientes para ser analizadas
for k in range(0, len(images)): 
    
    imgName = images[k];
    im = rs.open(imgName)
    
    coastal = im.read(1).astype('float64')
    blue = im.read(2).astype('float64')
    green = im.read(3).astype('float64')
    red = im.read(4).astype('float64')
    nir = im.read(5).astype('float64')
    swir1 = im.read(6).astype('float64')
    swir2 = im.read(7).astype('float64')
    
    y, x = blue.shape
    rgb = np.zeros(shape=(3,y,x))
    rgb[0,:,:] = red
    rgb[1,:,:] = green
    rgb[2,:,:] = blue
    
    rgb = np.uint16(rgb / 256)
    plot.show(rgb)    
    
    cloud = (red + green + blue) / 3
    im_cloud = np.float64(cloud / 256)
    #plot.show(im_cloud)    
    
    l = 55
    im_cloud[im_cloud < l] = 0
    im_cloud[im_cloud >= l] = 1
    plot.show(im_cloud)
    
    clouds[k] = im_cloud
    
# Fin for

# Combinar los pixeles de nubes
im_cloud = np.zeros(shape=(y,x))
for k in range(0, len(clouds)): 
    im_cloud[clouds[k] > 0] = 1 
    
plot.show(im_cloud)    
    
    
    
    
    
    
    
    
    
    
    