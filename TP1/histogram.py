#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:01:16 2025

@author: ecarrot
"""

import numpy as np

def dataHistogram(data, strConfig, configValue):
    # Le calcul des intervalles 'bins' se fait en fonction du paramètre strConfig donné par l'utilisateur:
    # Usage: [histoEdges, histoCenters, histoEff] = Histogram1(Tab1Dim, 'BinWidth', BinWidthValue)
    #Usage : [histoEdges, histoCenters, histoEff] = Histogram1(Tab1Dim, 'NbBin', NbBinValue)
    
    # 1- On calcule histoEdges et histoCenters
    # Ce calcul dépend du paramètre strConfig
    valMin = np.min(data)
    valMax = np.max(data) + np.finfo(float).eps
    valRange = valMax - valMin
    
    if (strConfig.lower() == "nbbin"):
        intervalLength = valRange / configValue
        nbBin = configValue
    elif (strConfig.lower() == "binwidth"):
        intervalLength = configValue
        nbBin = int(np.ceil(valRange))
        
    # On remplie histoEdges et histoCenters
    histoEdges = np.zeros(nbBin+1)
    histoCenters = np.zeros(nbBin)
    for k in range(0, nbBin):
        histoEdges[k]   = valMin + k * intervalLength
        histoCenters[k] = histoEdges[k] + intervalLength / 2
    histoEdges[nbBin] = histoEdges[nbBin-1] + intervalLength   

    # 2- On rempli l'histogramme lui-même en utilisant np.where...
    # Tip: remplir d'abord les bins de 0 à n-1 et faire un traitement particulier pour le dernier bin...
    histoEff = np.zeros(nbBin)
    for k in range(0, nbBin-1):
        histoEff[k] = np.size(np.where((histoEdges[k] <= data) & (data < histoEdges[k+1])))

    histoEff[nbBin-1] = np.size(np.where((histoEdges[nbBin-1] <= data)))
    
    return [histoEdges, histoCenters, histoEff]    


class Histogram:
    _title = "Histogramme"
    _xlabel = "valeurs"
    _ylabel = "effectifs"
    _histoCenters = None
    _histoEff = None
    _ax = None
    _xmin = -1
    _xmax = -1
        
    def __init__(self, axes, data, strConfig = "BinWidth", configValue = 1):
        self._ax = axes
        self._setData(data, strConfig, configValue)
        
    def setTitle(self, t):
        self._title = t
    
    def setXLabel(self, xlabel):
        self._xlabel = xlabel
    
    def setYLabel(self, ylabel):
        self._ylabel = ylabel
    
    def SetXRange(self, xmin, xmax):
        self._xmin = xmin
        self._xmax = xmax
    
    def _setData(self, data, strConfig = "BinWidth", configValue = 1):
        [_, self._histoCenters, self._histoEff] = dataHistogram(data, strConfig, configValue)
    
    def reDraw(self):
        self._ax.clear()
        self._ax.grid()
        self._ax.set_title(self._title)
        self._ax.set_xlabel(self._xlabel)
        self._ax.set_ylabel(self._ylabel)
        self._ax.bar(self._histoCenters, self._histoEff)
        if (self._xmin < self._xmax):
            ymax = np.max(self._histoEff) + 50
            self._ax.axis([self._xmin, self._xmax, 0, ymax])
