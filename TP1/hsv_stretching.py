#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 11:56:44 2025

@author: ecarrot
"""

import sys
from matplotlib import pyplot as plt
from images import HSVImg, RGBImg
from histogram import Histogram


def drawHisto(img, title, xminxmaxfixed, num_fig):
        # histo rouge
        hist1 = Histogram(img.getData()[:,:,0], "NbBin", 100)
        hist1.setTitle("Histogramme du canal Hue (Teinte)\nde " + title)
        hist1.setXLabel("code de la nuance")
        hist1.setYLabel("effectif (en nombre de pixels)")
        
        # histo vert
        hist2 = Histogram(img.getData()[:,:,1], "NbBin", 100)
        hist2.setTitle("Histogramme du canal Saturation\nde "+ title)
        hist2.setXLabel("code de la nuance")
        hist2.setYLabel("effectif (en nombre de pixels)")
        
        # histo vert
        hist3 = Histogram(img.getData()[:,:,2], "NbBin", 100)
        hist3.setTitle("Histogramme du canal Value\nde " + title)
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
    
    if sys.argv.count("--help") != 0 or len(sys.argv) < 2:
        print("Usage : python3 "+ sys.argv[0] +" fichier.png [-C] [-S] [-h] [-s] [-v] [-H] [-l] [-e cur_min cur_max]")
        print("With  :\n" + 
          "        -C : draw each channel separately\n"+
          "        -S : draw stretched image \n" +
          "        -H : draw histograms\n"+
          "        -l : draw histograms set axis between 0 and 255 \n"+
          "        -e xmin xmax\n"+
          "        -h : stretch h channel\n"+
          "        -s : stretch s channel\n"+
          "        -v : stretch v channel")
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
    
    
    h_channel = False
    if sys.argv.count("-h"):
        h_channel = True
    
    s_channel = False
    if sys.argv.count("-s"):
        s_channel = True
    
    v_channel = False
    if sys.argv.count("-v"):
        v_channel = True
    
    
    num_fig = 1
    
    imgrgb = RGBImg()
    imgrgb.setDataFrom(sys.argv[1])
    imghsv = HSVImg()
    imghsv.setDataFromRGBImg(imgrgb)
    
    # image originale
    fig = plt.figure(num_fig)
    num_fig += 1
    imghsv.setTitle("Image originale")
    imghsv.draw(plt.gca())
    
    
    # chaque canal image
    if draw_channels:
        fig = plt.figure(num_fig)
        num_fig += 1
        imghsv.drawEachChannel(fig, "Canaux Hue, Saturation, Value\nde l'image originale")
    
    
    # histogramme image original
    if (draw_histo):
        num_fig = drawHisto(imghsv, "l'image originale", xminxmaxfixed, num_fig)
    
    # image étallée
    if (strechtImg):
        plt.figure(num_fig)
        num_fig += 1
        
        img2 = imghsv.getStretchedImg(h_channel, s_channel, v_channel, 0, 255, xmin, xmax)
        img2.setTitle("Image après étalement")
        
        img2.draw(plt.gca())
        
        if (draw_histo):
            num_fig = drawHisto(img2, "l'image après étalement", xminxmaxfixed, num_fig)
            
        if draw_channels:
            fig = plt.figure(num_fig)
            num_fig += 1
            img2.drawEachChannel(fig, "Canaux HSV de l'image après étalement")  
    
    
    plt.show()
