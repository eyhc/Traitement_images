#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 20:31:35 2025

@author: ecarrot
"""

import sys
from matplotlib import pyplot as plt
from images import GrayImg
from histogram import Histogram


if __name__ == '__main__':
    
    if sys.argv.count("-h") != 0 or len(sys.argv) < 2:
        print("Usage : python3 "+ sys.argv[0] +" fichier.png [-s] [-H] [-l] [-S cur_min cur_max]")
        print("With  :\n" + 
          "        -s : draw stretched image \n" +
          "        -H : draw histograms\n"+
          "        -l : draw histograms set axis between 0 and 255 \n"+
          "        -S xmin xmax")
        if (len(sys.argv) < 2):
            sys.exit(1)
        else:
            sys.exit(0)
        
    
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
    img = GrayImg(fig.gca())
    img.setTitle("Image originale")
    img.setDataFrom(sys.argv[1])
    img.reDraw()
    
    # histogramme image original
    if (draw_histo):
        fig = plt.figure(num_fig)
        num_fig += 1
        hist = Histogram(fig.gca(), img.getData())
        hist.setTitle("Histogramme de l'image originale")
        hist.setXLabel("code de la nuance de gris")
        hist.setYLabel("effectif (en nombre de pixels)")
        if (xminxmaxfixed): hist.SetXRange(0, 255)
        hist.reDraw()
        
    # image étallée
    if (strechtImg):
        fig = plt.figure(num_fig)
        num_fig += 1
        img2 = img.getStretchedImg(fig.gca(), 0, 255, xmin, xmax)
        img2.setTitle("Image aprés étalement")
        img2.reDraw()
        if (draw_histo):
            fig = plt.figure(num_fig)
            num_fig += 1
            hist = Histogram(fig.gca(), img2.getData())
            hist.setTitle("Histogramme après étalement")
            hist.setXLabel("code de la nuance de gris")
            hist.setYLabel("effectif (en nombre de pixels)")
            if (xminxmaxfixed): hist.SetXRange(0, 255)
            hist.reDraw()

    plt.show()
