#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 10:40:42 2018

@author: celine fouard et elie carrot
"""
import numpy as np


def Conv1D(x, h, shape):
    #Usage : z = Conv1D(x, h, shape)
    #Return the convolution between x and h with Nx+Nh-1 samples
    #shape : 'valid', 'same', 'full'

    Nx = len(x)
    Nh = len(h)
    SizeEffect = Nh // 2
    
    # On "retourne" h
    hPrime = np.flip(h)
    
    # On calcule de base y 'full'.
    # On déduira les autres configurations à partir de celle-ci.
    # Du coup, on complète x avec des zéros de chaque côté, de la taille du noyau - 1
    NFull = Nx + 2 * (Nh-1)
    xFull = np.zeros(NFull)
    xFull[Nh-1 : Nh-1 + Nx] = x
    
    # On crée y de la taille maximale, c'est-à-dire Nx + Nh-1
    y = np.zeros(Nx+Nh-1)
    
    # On calcule la valeur de chaque point d'y
    for i in range(0, Nx+Nh-1):
        y[i] = np.sum(xFull[i:i+Nh] * hPrime)
        
    
    # On renvoie un vecteur plus ou moins tronqué selon la configuration
    if 'valid' in shape.lower(): 
        z = y[Nh-1 : Nx]
        
    elif 'same' in shape.lower():
        z = y[SizeEffect: Nx +SizeEffect]
        
    elif 'full' in shape.lower():  
        z = y

    return z

def Conv2D(x, h, shape):
    #Usage : z = Conv2D(x, h, shape)
    #Return the convolution between x and h with Nx+Nh-1 samples
    #shape : 'valid', 'same', 'full'

    Nx = np.shape(x)
    Nh = np.shape(h)
    
    SizeEffect = np.zeros(2, dtype = int)
    SizeEffect[0] = int(Nh[0] // 2)
    SizeEffect[1] = int(Nh[1] // 2)
    
    # on "retourne" h
    hPrime = np.flip(h, (0,1))
    
    NFull = (Nx[0] + 2*(Nh[0]-1), Nx[1] + 2*(Nh[1]-1))
    xFull = np.zeros(NFull)
    xFull[Nh[0]-1:Nh[0]-1 + Nx[0], Nh[1]-1 : Nh[1]-1 + Nx[1]] = x
    
    y = np.zeros((Nx[0] + Nh[0]-1, Nx[1] + Nh[1]-1))
    
    for i in range(0, Nx[0]+Nh[0]-1):
        for j in range(0, Nx[1]+Nh[1]-1):
            y[i,j] = np.sum(xFull[i:i+Nh[0], j:j+Nh[1]] * hPrime)
        
    if 'valid' in shape.lower(): 
        z = y[Nh[0]-1 : Nx[0], Nh[1]-1 : Nx[1]]
        
    elif 'same' in shape.lower():
        z = y[SizeEffect[0]: SizeEffect[0] + Nx[0], SizeEffect[1]: SizeEffect[1] + Nx[1]]
        
    elif 'full' in shape.lower():  
        z = y;

    return z
