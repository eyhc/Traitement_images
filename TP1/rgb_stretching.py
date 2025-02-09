#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:31:35 2025

@author: ecarrot
"""

import sys
from matplotlib import pyplot as plt
from images import RGBImg
from histogram import Histogram


def drawHisto(img, title, xminxmaxfixed, num_fig):
        # histo rouge
        hist1 = Histogram(img.getData()[:,:,0], "NbBin", 100)
        hist1.setTitle("Histogramme du canal rouge\nde " + title)
        hist1.setXLabel("code de la nuance")
        hist1.setYLabel("effectif (en nombre de pixels)")
        
        # histo vert
        hist2 = Histogram(img.getData()[:,:,1], "NbBin", 100)
        hist2.setTitle("Histogramme du canal vert\nde "+ title)
        hist2.setXLabel("code de la nuance")
        hist2.setYLabel("effectif (en nombre de pixels)")
        
        # histo vert
        hist3 = Histogram(img.getData()[:,:,2], "NbBin", 100)
        hist3.setTitle("Histogramme du canal bleu\nde " + title)
        hist3.setXLabel("code de la nuance")
        hist3.setYLabel("effectif (en nombre de pixels)")
        
        if (xminxmaxfixed):
            hist1.SetXRange(0, 255)
            hist2.SetXRange(0, 255)
            hist3.SetXRange(0, 255)
        
        plt.figure(num_fig)
        num_fig += 1
        hist1.draw(plt.gca())
        
        plt.figure(num_fig)
        num_fig += 1
        hist2.draw(plt.gca())
        
        plt.figure(num_fig)
        num_fig += 1
        hist3.draw(plt.gca())
        
        return num_fig


if __name__ == '__main__':
    
    if sys.argv.count("-h") != 0 or len(sys.argv) < 2:
        print("Usage : python3 "+ sys.argv[0] +" fichier.png [-C] [-s] [-H] [-l] [-S cur_min cur_max]")
        print("With  :\n" + 
          "        -C : draw each channel separately\n"+
          "        -s : draw stretched image \n" +
          "        -H : draw histograms\n"+
          "        -l : draw histograms set axis between 0 and 255 \n"+
          "        -S xmin xmax")
        if (len(sys.argv) < 2):
            sys.exit(1)
        else:
            sys.exit(0)
        
    draw_channels = False
    if sys.argv.count("-C") > 0:
        draw_channels = True
    
    draw_histo = False
    if (sys.argv.count("-H") > 0):
        draw_histo = True
    
    strechtImg = False
    if (sys.argv.count("-s") > 0):
        strechtImg = True
        
    xminxmaxfixed = False
    if (sys.argv.count("-l") > 0):
        xminxmaxfixed = True

    xmin = -1
    xmax = -1
    
    if sys.argv.count("-S"):
        i = sys.argv.index("-S")
        xmin = int(sys.argv[i+1])
        xmax = int(sys.argv[i+2])
    
    num_fig = 1
    
    # image originale
    fig = plt.figure(num_fig)
    num_fig += 1
    img = RGBImg()
    img.setTitle("Image originale")
    img.setDataFrom(sys.argv[1])
    img.draw(plt.gca())
    
    
    # chaque canal image
    if draw_channels:
        fig = plt.figure(num_fig)
        num_fig += 1
        img.drawEachChannel(fig, "Canaux rouge, vert et bleu de l'image originale")
    
    
    # histogramme image original
    if (draw_histo):
        num_fig = drawHisto(img, "l'image originale", xminxmaxfixed, num_fig)
    
    # image étallée
    if (strechtImg):
        plt.figure(num_fig)
        num_fig += 1
        
        img2 = img.getStretchedImg(0, 255, xmin, xmax)
        if xmin != xmax:
            img2.setTitle("Image après étalement uniforme\nsur tous les canaux")
        else:
            img2.setTitle("Image après étalement sur\nchaque canaux indépendamment")
        
        img2.draw(plt.gca())
        
        if (draw_histo):
            num_fig = drawHisto(img2, "l'image après étalement", xminxmaxfixed, num_fig)
            
        if draw_channels:
            fig = plt.figure(num_fig)
            num_fig += 1
            img2.drawEachChannel(fig, "Canaux rouge, vert et bleu de l'image après étalement")
            

    plt.show()
