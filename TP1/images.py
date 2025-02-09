#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:58:12 2025

@author: ecarrot
"""

import matplotlib.image as mpimg
import numpy as np


def Image1ChannelStretching(imaIn, newMin, newMax, curMin, curMax):
    shape = imaIn.shape
    imaOut = np.copy(imaIn).reshape(-1)
    for i in range(imaOut.size):
        imaOut[i] = max(imaOut[i], curMin)
        imaOut[i] = min(imaOut[i], curMax)
        imaOut[i] = newMin + (imaOut[i]-curMin) * ((newMax-newMin)/(curMax-curMin))
    return np.reshape(imaOut, shape)


class GrayImg:
    def __init__(self):
        self._title = -1
        
    def setDataFrom(self, path):
        self._img = mpimg.imread(path)
        if self._img.dtype == np.float32:
            self._img = (self._img * 255).astype(np.uint8)
        
    def setData(self, img):
        self._img = img
        
    def setTitle(self, t):
        self._title = t
        
    def draw(self, axes):
        axes.clear()
        if (self._title != -1):
            axes.set_title(self._title)
        axes.imshow(self._img, vmin=0, vmax=255, cmap='gray')
        
    def getData(self):
        return self._img
        
    def getStretchedImg(self, new_min=0, new_max=255, curr_min=-1, curr_max=-1):
        mi = curr_min
        if (mi == -1):
            mi = np.min(self._img)
        ma = curr_max
        if (ma == -1):
            ma = np.max(self._img)
        imgstretched = Image1ChannelStretching(self._img, new_min, new_max, mi, ma)
        img = GrayImg()
        img.setData(imgstretched)
        return img


class RGBImg:
    def __init__(self):
        self._title = -1
        
    def setDataFrom(self, path):
        self._img = mpimg.imread(path)
        if self._img.dtype == np.float32:
            self._img = (self._img * 255).astype(np.uint8)
    
    def setData(self, img):
        self._img = img
    
    def setTitle(self, t):
        self._title = t
    
    def draw(self, axes):
        axes.clear()
        if (self._title != -1):
            axes.set_title(self._title)
        axes.imshow(self._img, vmin=0, vmax=255)
        
    def drawEachChannel(self, figure, title = -1):
        ax1, ax2, ax3 = figure.subplots(1, 3, sharey=True)
        ax1.imshow(self._img[:,:,0], vmin=0, vmax=255, cmap='gray')
        ax1.set_title('Canal rouge')
        ax2.imshow(self._img[:,:,1], vmin=0, vmax=255, cmap='gray')
        ax2.set_title('Canal vert')
        ax3.imshow(self._img[:,:,2], vmin=0, vmax=255, cmap='gray')
        ax3.set_title('Canal bleu')
        if title != -1:
            figure.suptitle(title)
            
    def getStretchedImg(self, new_min=0, new_max=255, curr_min=-1, curr_max=-1):
        redchannel = self._img[:,:,0]
        mi = curr_min; ma = curr_max
        if (mi == -1): mi = np.min(redchannel)
        if (ma == -1): ma = np.max(redchannel)
        imgstretchedred = Image1ChannelStretching(redchannel, new_min, new_max, mi, ma)
        
        greenchannel = self._img[:,:,1]
        mi = curr_min; ma = curr_max
        if (mi == -1): mi = np.min(greenchannel)
        if (ma == -1): ma = np.max(greenchannel)
        imgstretchedgreen = Image1ChannelStretching(greenchannel, new_min, new_max, mi, ma)
        
        bluechannel = self._img[:,:,2]
        mi = curr_min; ma = curr_max
        if (mi == -1): mi = np.min(bluechannel)
        if (ma == -1): ma = np.max(bluechannel)
        imgstretchedblue = Image1ChannelStretching(bluechannel, new_min, new_max, mi, ma)
        
        imgstretched = np.array(np.zeros(self._img.shape), dtype='uint8')
        imgstretched[:,:,0] = imgstretchedred
        imgstretched[:,:,1] = imgstretchedgreen
        imgstretched[:,:,2] = imgstretchedblue
        
        img = RGBImg()
        img.setData(imgstretched)
        return img
    
    def getData(self):
        return self._img


class YCbCrImg:
    def __init__(self):
        self._title = -1
    
    def setDataFromRGBImg(self, rgbimg):
        self._img = rgbimg
        
    def getRGBImg(self):
        return None
    
    def setData(self, img):
        self._img = img
    
    def setTitle(self, t):
        self._title = t
    
    def draw(self, axes):
        axes.clear()
        if (self._title != -1):
            axes.set_title(self._title)
        axes.imshow(self._img, vmin=0, vmax=255)
        
    def drawEachChannel(self, figure, title = -1):
        ax1, ax2, ax3 = figure.subplots(1, 3, sharey=True)
        ax1.imshow(self._img[:,:,0], vmin=0, vmax=255, cmap='gray')
        ax1.set_title('Canal Y')
        ax2.imshow(self._img[:,:,1], vmin=0, vmax=255, cmap='gray')
        ax2.set_title('Canal Cb')
        ax3.imshow(self._img[:,:,2], vmin=0, vmax=255, cmap='gray')
        ax3.set_title('Canal Cr')
        if title != -1:
            figure.suptitle(title)
    """       
    def getStretchedImg(self, new_min=0, new_max=255, curr_min=-1, curr_max=-1):
        redchannel = self._img[:,:,0]
        mi = curr_min; ma = curr_max
        if (mi == -1): mi = np.min(redchannel)
        if (ma == -1): ma = np.max(redchannel)
        imgstretchedred = Image1ChannelStretching(redchannel, new_min, new_max, mi, ma)
        
        greenchannel = self._img[:,:,1]
        mi = curr_min; ma = curr_max
        if (mi == -1): mi = np.min(greenchannel)
        if (ma == -1): ma = np.max(greenchannel)
        imgstretchedgreen = Image1ChannelStretching(greenchannel, new_min, new_max, mi, ma)
        
        bluechannel = self._img[:,:,2]
        mi = curr_min; ma = curr_max
        if (mi == -1): mi = np.min(bluechannel)
        if (ma == -1): ma = np.max(bluechannel)
        imgstretchedblue = Image1ChannelStretching(bluechannel, new_min, new_max, mi, ma)
        
        imgstretched = np.array(np.zeros(self._img.shape), dtype='uint8')
        imgstretched[:,:,0] = imgstretchedred
        imgstretched[:,:,1] = imgstretchedgreen
        imgstretched[:,:,2] = imgstretchedblue
        
        img = RGBImg()
        img.setData(imgstretched)
        return img
    """
    
    def getData(self):
        return self._img

class HSVImg:
    def __init__(self):
        self._title = -1

