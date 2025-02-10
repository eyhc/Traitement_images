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
        print("Usage : python3 "+ sys.argv[0] +" fichier.png [-S] [-H] [-l] [-e cur_min cur_max]")
        print("With  :\n" + 
          "        -S : draw stretched image \n" +
          "        -H : draw histograms\n"+
          "        -l : draw histograms set axis between 0 and 255 \n"+
          "        -e xmin xmax")
        if (len(sys.argv) < 2):
            sys.exit(1)
        else:
            sys.exit(0)
        
    
    draw_histo = False
    if (sys.argv.count("-H") > 0):
        draw_histo = True
    
    strechtImg = False
    if (sys.argv.count("-S") > 0):
        strechtImg = True
        
    xminxmaxfixed = False
    if (sys.argv.count("-l") > 0):
        xminxmaxfixed = True

    xmin = -1
    xmax = -1
    
    if sys.argv.count("-e"):
        i = sys.argv.index("-e")
        xmin = int(sys.argv[i+1])
        xmax = int(sys.argv[i+2])
    
    num_fig = 1
    
    # image originale
    fig = plt.figure(num_fig)
    num_fig += 1
    img = GrayImg()
    img.setTitle("Image originale")
    img.setDataFrom(sys.argv[1])
    img.draw(fig.gca())
    
    # histogramme image original
    if (draw_histo):
        fig = plt.figure(num_fig)
        num_fig += 1
        hist = Histogram(img.getData())
        hist.setTitle("Histogramme de l'image originale")
        hist.setXLabel("code de la nuance de gris")
        hist.setYLabel("effectif (en nombre de pixels)")
        if (xminxmaxfixed): hist.SetXRange(0, 255)
        hist.draw(fig.gca())
    
    # image étallée
    if (strechtImg):
        fig = plt.figure(num_fig)
        num_fig += 1
        img2 = img.getStretchedImg(0, 255, xmin, xmax)
        img2.setTitle("Image aprés étalement")
        img2.draw(fig.gca())
        if (draw_histo):
            fig = plt.figure(num_fig)
            num_fig += 1
            hist = Histogram(img2.getData())
            hist.setTitle("Histogramme après étalement")
            hist.setXLabel("code de la nuance de gris")
            hist.setYLabel("effectif (en nombre de pixels)")
            if (xminxmaxfixed): hist.SetXRange(0, 255)
            hist.draw(fig.gca())

    plt.show()
