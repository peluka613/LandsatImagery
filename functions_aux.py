#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 10:42:38 2019

@author: peluka
"""
from PIL import Image
import numpy as np # Vector and matrix
import matplotlib.pyplot as plt # View images inside spyder
import PIL
import scipy.signal as sg
from scipy.ndimage import filters
import cv2
from sklearn.cluster import KMeans
#=========================================================
#=========================================================

def printc(image):
    plt.imshow(image)
    plt.axis("off")
    #=========================================================
def printc_title(image, title):
    plt.title(title)
    plt.imshow(image)
    plt.axis("off")
#=========================================================
def printc_no_override(image):
    plt.figure() # Do not override images
    printc(image)
    #=========================================================
def printc_no_override_title(image, title):
    plt.figure() # Do not override images
    printc_title(image, title)
#=========================================================
def print_gray(image):
    plt.imshow(image,cmap='gray')
    plt.axis("off")
    #=========================================================
def print_gray_title(image, title):
    plt.title(title)
    plt.imshow(image,cmap='gray')
    plt.axis("off")
#=========================================================
def print_gray_no_override(image):
    plt.figure() # Do not override images
    print_gray(image)
    #=========================================================
def print_gray_no_override_title(image, title):
    plt.figure() # Do not override images
    print_gray_title(image, title)
#=========================================================
# FUNCION INVERSA
def my_inversa(image):
    Im_ga = np.double(image)
    Im2 = 255 - Im_ga # Invert imge
    return Im2   
#=========================================================
def binary_diference(im1, im2):
    [row, col] = im1.shape;
    image = np.copy(im1)
    
    for i in range(0,row-1):
        for j in range(0,col-1):  
            if(im2[i, j] != 0):
                image[i, j]  = 0
                
    return np.uint16(image)              
                 

#=========================================================
    
    
#=========================================================
#=========================================================
# FUNCIÓN GAMMA
def my_gamma(image, gamma):
    Im_ga = np.double(image)
    Im2 = Im_ga**gamma #gamma image
    Im2 = np.uint8(255 * Im2 / Im2.max())
    return Im2
#=========================================================
#=========================================================
# Contar
def contPixBinario(im):
    Size = im.size
    Objeto = np.count_nonzero(im)    
    Fondo = Size - Objeto
    
    return (Size, Objeto, Fondo)    
#=========================================================       
#=========================================================    
    
# KMeans
def myKMeansCopy(espaces, titles, N): #SE TOMAN TODOS LOS ESPACIOS ANTERIORES
    for k in range(0, len(espaces)):
        img = espaces[k] 
        [nf,nc] = img.shape #NUMERO DE FILAS, NUMERO DE COLUMNAS Y LOS CANALES
        printc_no_override_title(espaces[k], titles[k]) 
        #----------------------------------------------------
        
        img2 = np.reshape(img,(nf*nc,1)) 
        kmeans = KMeans(n_clusters=N, random_state=0).fit(img2) 
        C = kmeans.labels_
        
        imgC = np.reshape(C,(nf,nc)) 
        #printc_no_override_title(imgC, titles[k] + " imgC") #MUESTRA LA IMGN
        
        for i in range(0,N):
            mask = np.zeros(imgC.shape,np.uint8)
            mask[imgC==i] = 255
            
            [Size, Objeto, Fondo] = contPixBinario(mask)
            conteo = ' Size = ' + str(Size) + ' Objeto = ' + str(Objeto) + ' Fondo = ' + str(Fondo)
            
            print_gray_no_override_title(mask, titles[k] + " It " + str(i) + conteo) #MUESTRA LA IMAGEN CON SU RESPECTIVO NÚMERO DE PIXELES
            
#=========================================================
#=========================================================   
            
def myKMeansGetC(img, N):
    [nf,nc] = img.shape #NUMERO DE FILAS, NUMERO DE COLUMNAS
    #----------------------------------------------------
    
    img2 = np.reshape(img,(nf*nc,1)) 
    kmeans = KMeans(n_clusters=N, random_state=0).fit(img2) 
    C = kmeans.labels_
    
    imgC = np.reshape(C,(nf,nc)) 
    
    return imgC
#=========================================================    
    
def myKMeansArray(espaces, titles, N): #SE TOMAN TODOS LOS ESPACIOS
    for k in range(0, len(espaces)):
        myKMeans(espaces[k], titles[k], N)
                   
#=========================================================    

def myKMeansArrayOnlyIt(espaces, titles, N, i): #SE TOMAN TODOS LOS ESPACIOS
    for k in range(0, len(espaces)):
        mask = myKMeansByIt(espaces[k], N, i)
        print_gray_no_override_title(mask, titles[k] + " It " + str(i))           
#=========================================================         
                
def myKMeans(img, title, N): 
    for i in range(0,N):
        mask = myKMeansByIt(img, N, i)            
        print_gray_no_override_title(mask, title + " It " + str(i))     
#=========================================================        

def myKMeansByIt(img, N, i): 
    imgC = myKMeansGetC(img, N)
    mask = np.zeros(imgC.shape,np.uint16)
    mask[imgC==i] = 255
    
    return mask
            
#=========================================================
    