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
    def __init__(self, axes):
        self._ax = axes
        self._title = -1
        
    def setDataFrom(self, path):
        self._img = mpimg.imread(path)
        if self._img.dtype == np.float32:
            self._img = (self._img * 255).astype(np.uint8)
        
    def setData(self, img):
        self._img = img
        
    def setTitle(self, t):
        self._title = t
        
    def reDraw(self):
        self._ax.clear()
        if (self._title != -1):
            self._ax.set_title(self._title)
        self._ax.imshow(self._img, vmin=0, vmax=255, cmap='gray')
        
    def getData(self):
        return self._img
        
    def getStretchedImg(self, new_axes, new_min=0, new_max=255, curr_min=-1, curr_max=-1):
        mi = curr_min
        if (mi == -1):
            mi = np.min(self._img)
        ma = curr_max
        if (ma == -1):
            ma = np.max(self._img)
        imgstretched = Image1ChannelStretching(self._img, new_min, new_max, mi, ma)
        img = GrayImg(new_axes)
        img.setData(imgstretched)
        return img
