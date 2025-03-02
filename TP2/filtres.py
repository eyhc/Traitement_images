#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 19:30:21 2025

@author: celine fouard et elie carrot
"""

import numpy as np
from convolution import Conv1D, Conv2D


def noyauBinomial(n):
    base = np.array([1,1])
    result = np.copy(base)
    
    for _ in range(n-1):
        result = Conv1D(result, base, 'full')
    
    kern = np.zeros((n+1,n+1))
    
    for i in range(n+1):
        kern[i][:] = result[i] * result
    
    return kern / np.sum(kern)


def noyauGaussien(sigma):
    sigma = sigma + np.finfo(float).eps
    def f(x,y):
        return np.exp(-(x*x+y*y)/(2*sigma*sigma))
    
    n = int(np.floor(2*sigma))
    mi = -n
    ma = n
    X,Y = np.mgrid[mi:ma, mi:ma]
    noyau = f(X,Y)
    return noyau / np.sum(noyau)

    
def noyauMoyenne(n):
    return np.ones((n,n)) / (n*n)


def noyauLaplace(nom='4-connexe'):
    h = np.zeros((3,3))
    base = np.array([1, -2, 1])
    if nom == '8-connexe':
        h += 1
        h[1][1] = -8
    elif nom == 'robinson':
        h[0,:] = base
        h[1,:] = -2 * base
        h[2,:] = base
    elif nom == 'binomial':
        h[:,:] = noyauLaplace('4-connexe') + noyauLaplace('8-connexe')
    else:
        h[1,:] = base
        h[:,1] += base

    return h


#######################################################################

def filtreMoyenne(img: np.array, n: np.uint8):
    # n+1 est la largeur et la hauteur du noyau
    n += 1
    h = noyauMoyenne(n)
    return Conv2D(img, h, 'same')


def filtreBinomial(img: np.array, n: np.uint8):
    # n est l'ordre du noyau (sa largeur et hauteur)
    h = noyauBinomial(n)
    return Conv2D(img, h, 'same')

def filtreGaussien(img: np.array, sigma: np.float32):
    h = noyauGaussien(sigma)
    return Conv2D(img, h, 'same')


def filtreRoberts(img):
    D = np.array([1,-1])
    # on récupère la matrice en niveaux de gris
    shape = np.shape(img)
 
    # Application du filtre de Roberts en ligne
    robertsX = np.zeros((shape[0], shape[1]), np.dtype(int))
    # D étant 1D, il faut convoluer ligne par ligne
    for li in range(robertsX.shape[0]):
        robertsX[li,:] = Conv1D(img[li,:], D, 'same')
 
    # Application du filtre de Roberts en colonne
    robertsY = np.zeros((shape[0], shape[1]), np.dtype(int))
    # D étant 1D, il faut convoluer colonne par colonne
    for col in range(robertsY.shape[1]):
        robertsY[:,col] = Conv1D(img[:,col], D, 'same')
 
    # Calcul de la norme du filtre
    robertsN = np.zeros((shape[0], shape[1]), float)
    # Chaque pixel de robertsN est égal à sqrt( robertsX^2 * robertsY^2 )
    for li in range(img.shape[0]):
        for col in range(img.shape[1]):
            robertsN[li,col] = np.sqrt(robertsX[li, col]*robertsX[li, col] + robertsY[li, col]*robertsY[li, col])
 
    return robertsX, robertsY, robertsN



def filtreSobel(img: np.array):
    # Ici le filtrage est 2D.
    # Fitre de Sobel 2D en lignes
    Gx = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]) * 1/4
    # Filgre de Sobel 2D en colonnnes
    Gy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) * 1/4

    # On crée une image 2D pour le filtre de Sobel en lignes
    sobelX = np.zeros((img.shape[0], img.shape[1]), np.dtype(int))
    sobelX = Conv2D(img, Gx, 'same')

    # On crée une image 2D pour le filtre de Sobel en colonnes
    sobelY = np.zeros((img.shape[0], img.shape[1]), np.dtype(int))
    sobelY = Conv2D(img, Gy, 'same')

    # On calcule la norme de ces 2 images
    sobelN = np.zeros((img.shape[0], img.shape[1]), np.dtype(float))
    for li in range(img.shape[0]):
        for col in range(img.shape[1]):
            sobelN[li, col] = np.sqrt(sobelX[li, col]*sobelX[li, col] + sobelY[li, col]*sobelY[li, col])

    return sobelX, sobelY, sobelN


def filtreLaplacien(img: np.array, noyau='4-connexe'):
    h = noyauLaplace(noyau)
    return Conv2D(img, h, 'same')


def filtreLaplacienRehausseur(img: np.array, alpha=0.1, noyau='4-connexe'):
    return img - alpha * filtreLaplacien(img, noyau)
    