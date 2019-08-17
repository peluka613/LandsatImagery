#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 17:18:56 2019

@author: peluka
"""

from glob import glob
import os

import numpy.ma as ma
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches as mpatches, colors
from matplotlib.colors import ListedColormap
import matplotlib as mpl
import seaborn as sns

import rasterio as rio
from rasterio.plot import plotting_extent
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping

import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

plt.ion()
sns.set_style('white')
sns.set(font_scale=1.5)

#os.chdir(os.path.join(et.io.HOME, 'earth-analytics'))
"""
# Stack the landsat pre fire data
landsat_paths_pre = glob(
    "data/cold-springs-fire/landsat_collect/LC080340322016070701T1-SC20180214145604/crop/*band*.tif")
path_landsat_pre_st = 'data/cold-springs-fire/outputs/landsat_pre_st.tif'
es.stack_raster_tifs(landsat_paths_pre, path_landsat_pre_st, arr_out=False)
"""
imgName1 = '170323'
imgName2 = '170324'
imgName3 = '170614'
imgName4 = '171224'
imgName5 = '180615'

imgName = imgName1+ '.tif'

# Read landsat pre fire data
with rio.open(imgName) as landsat_pre_src:
    landsat_pre = landsat_pre_src.read(masked=True)
    landsat_extent = plotting_extent(landsat_pre_src)
    
    
    
# Define Landast bands for plotting homework plot 1
landsat_rgb = [3, 2, 1]

fig, ax = plt.subplots(1, 1, figsize=(10, 6))

ep.plot_rgb(landsat_pre,
            rgb=landsat_rgb,
            ax=ax,
            extent=landsat_extent)
ax.set(title=imgName)
ax.set_axis_off()
plt.show()    
    
    
    
    
print('Finished!')    