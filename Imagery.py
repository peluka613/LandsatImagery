#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:59:34 2019

@author: peluka
"""

#import functions as fn
import rasterio as rs
from rasterio import plot
import numpy as np

import matplotlib.pyplot as plt 
import copy

# Lista de imágenes a procesar
names = np.array(['170323.tif', '170324.tif', '170614.tif', '171224.tif', '180615.tif'])
#names = np.array(['170323.tif'])

# Arreglos para contener las imágenes procesadas
images = [None] * len(names)
rgbs = [None] * len(names)
clouds = [None] * len(names)
clouds = [None] * len(names)
ndvi = [None] * len(names)
mndwi = [None] * len(names)
ui = [None] * len(names)

x = 0
y = 0

cmap1 = copy.copy(plt.cm.rainbow)
print(cmap1)

#=============================================================
# Recorrer la lista de imágenes
for k in range(0, len(names)): 
    
    #=========================================================
    # Leer imagen y separar bandas
    imgName = names[k];
    im = rs.open(imgName)
    images[k] = im
    
    blue = im.read(2).astype('float64')
    green = im.read(3).astype('float64')
    red = im.read(4).astype('float64')
    
    #=========================================================
    # Obtener píxeles cubiertos por nubes
    cloud = (red + green + blue) / 3
    im_cloud = np.float64(cloud / 256)
    
    l = 55
    im_cloud[im_cloud < l] = 0
    im_cloud[im_cloud >= l] = 1
    #plot.show(im_cloud)
    
    clouds[k] = im_cloud
    
# Fin for
#=============================================================

# Combinar los pixeles de nubes
y, x = clouds[0].shape
im_cloud = np.zeros(shape=(y,x))
for k in range(0, len(clouds)): 
    im_cloud[clouds[k] > 0] = 1 
 
plot.show(im_cloud, title='Clouds')    
    
    
#=============================================================
# Recorrer la lista de imágenes, procesarlas y agregarlas a los arreglos correspondientes para ser analizadas
for k in range(0, len(images)): 
    
    #=========================================================
    # Leer imagen y separar bandas 1-7   
    im = images[k]
    
    coastal = im.read(1).astype('float64')
    blue = im.read(2).astype('float64')
    green = im.read(3).astype('float64')
    red = im.read(4).astype('float64')
    nir = im.read(5).astype('float64')
    swir1 = im.read(6).astype('float64')
    swir2 = im.read(7).astype('float64')
    
   #=========================================================
    # Obtener imagen en RGB
    y, x = blue.shape
    rgb = np.zeros(shape=(3,y,x))
    rgb[0,:,:] = red
    rgb[1,:,:] = green
    rgb[2,:,:] = blue
    
    rgb = np.uint16(rgb / 256)
    rgbs[k] = rgb
    plot.show(rgb, cmap=cmap1, title=names[k] + ' - RGB')   
    
    #=========================================================
    # NDVI Vegetación
    ndvi[k] = (nir - red) / (nir + red)
    
    l = 0.3
    ndvi[k][ndvi[k] < l] = 0
    ndvi[k][ndvi[k] >= l] = 1
    
    # Quitar píxeles cubiertos por nubes
    ndvi[k][im_cloud == 1] = 0 
    
    plot.show(ndvi[k], title=names[k] + ' - NDVI')
    
    #=========================================================
    # MNDWI Water
    mndwi[k] = (green - swir1) / (green + swir1)
    
    l = 0.08
    mndwi[k][mndwi[k] < l] = 0
    mndwi[k][mndwi[k] >= l] = 1
    
    # Quitar píxeles cubiertos por nubes
    mndwi[k][im_cloud == 1] = 0 
    
    plot.show(mndwi[k], title=names[k] + ' - MNDWI')
    
    #=========================================================
    # UI Urban index
    ui[k] = (swir2 - nir) / (swir2 + nir)
    
    l = -0.1
    ui[k][ui[k] > l] = 1
    ui[k][ui[k] <= l] = 0
    
     # Quitar píxeles cubiertos por nubes
    ui[k][im_cloud == 1] = 0 
    
    plot.show(ui[k], title=names[k] + ' - UI')
    
# Fin for
#=============================================================    
    
    
    
    
    
    
    
    