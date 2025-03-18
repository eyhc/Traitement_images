#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 10:26:19 2025

@author: elie carrot
"""

import sys, os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import filtres

if __name__ == '__main__':
    
    valid_file = len(sys.argv) >= 2 and os.path.isfile(sys.argv[1])
    
    if sys.argv.count("-h") != 0 or not valid_file:
        print("Usage : python3 "+ sys.argv[0] +" image.png [-f filtre] [-p parametres_filtre] [-l numero]")
        print("With  :\n" + 
          "        -f : choisir un filtre parmi :\n" +
          "               o MOYENNE              - paramètres: enier: ordre du noyau\n" +
          "               o GAUSSIEN             - paramètres: float: sigma\n" +
          "               o BINOMIAL             - paramètres: entier: ordre du noyau\n" +
          "               o SOBEL                - paramètres: float: alpha \n" +
          "               o ROBERTS              - paramètres: float: alpha \n" +
          "               o LAPLACIEN            - paramètres: string: 4-connexe | 8-connexe | robinson | binomial\n" +
          "               o LAPLACIEN_REHAUSSEUR - paramètres: string float: idem_prec alpha \n" +
          "        -l : afficher le signal pour une ligne de l'image\n")
        if (not valid_file):
            sys.exit(1)
        else:
            sys.exit(0)
    

    # obtenir le filtre à appliquer
    filtre = -1
    if sys.argv.count("-f") > 0:
        i = sys.argv.index("-f")
        filtre_arg = sys.argv[i+1]
        
        if filtre_arg == "MOYENNE":
            filtre = 0
        elif filtre_arg == "BINOMIAL":
            filtre = 1
        elif filtre_arg == "GAUSSIEN":
            filtre = 2
        elif filtre_arg == "SOBEL":
            filtre = 3
        elif filtre_arg == "ROBERTS":
            filtre = 4
        elif filtre_arg == "LAPLACIEN":
            filtre = 5
        elif filtre_arg == "LAPLACIEN_REHAUSSEUR":
            filtre = 6
    
    
    # obtenir la ligne à afficher si définie
    draw_line_signal = -1
    if sys.argv.count("-l"):
        i = sys.argv.index("-l")
        draw_line_signal = int(sys.argv[i+1])
        
        
    # paramètre du filtre
    n = 5
    sigma = 0.1
    alpha = 0.1
    noyau = '4-connexe'
    nom_filtre = "filtre "
    
    if filtre == 0 or filtre == 1:
        if sys.argv.count("-p") != 0:
            i = sys.argv.index("-p")
            n = int(sys.argv[i+1])
        
        if filtre == 0:
            nom_filtre += "moyenne"
        else:
            nom_filtre += "binomial"    
        nom_filtre += " d'ordre " + str(n)
    
    elif filtre == 2:
        if sys.argv.count("-p") != 0:
            i = sys.argv.index("-p")
            sigma = float(sys.argv[i+1])
        
        nom_filtre += "gaussien, sigma=" + str(sigma)
        
    elif filtre == 3 or filtre == 4:
        if sys.argv.count("-p") != 0:
            i = sys.argv.index("-p")
            alpha = float(sys.argv[i+1])
        if filtre == 3:
            nom_filtre += "de Sobel"    
        elif filtre == 4:
            nom_filtre += "de Roberts"
        
    
    elif filtre == 5 or filtre == 6:
        if sys.argv.count("-p") != 0:
            i = sys.argv.index("-p")
            p = sys.argv[i+1]
            if p == "8-connexe" or p == "binomial" or p == "robinson":
                noyau = p
            if filtre == 6:
                alpha = float(sys.argv[i+2])
        
        nom_filtre += "laplacien"


    if filtre == 3 or filtre == 4 or filtre == 6:
        nom_filtre += " réhausseur" 

    if filtre == 5 or filtre == 6:
        nom_filtre += ", noyau=" + noyau
    
    if filtre == 3 or filtre == 4 or filtre == 6:
        nom_filtre += ", alpha=" + str(alpha)



    #########################################################################
    
    
    # open image
    img = mpimg.imread(sys.argv[1])
    if len(img.shape) == 3:
        img = img[:,:,0]
    if img.dtype == np.float32:
        img = (img * 255).astype(np.uint8)
        
    
    num_fig = 1
    
    # image originale
    fig = plt.figure(num_fig)
    num_fig += 1
    

    axes = plt.gca()
    axes.set_title("Image originale")
    axes.imshow(img, vmin=0, vmax=255, cmap='gray')
    
    
    # image filtrée
    if filtre != -1:
        # appliquer le filtre
        img2 = None
        imgX = None
        imgY = None
        if filtre == 0:
            img2 = filtres.filtreMoyenne(img, n)
        elif filtre == 1:
            img2 = filtres.filtreBinomial(img, n)
        elif filtre == 2:
            img2 = filtres.filtreGaussien(img, sigma)
        elif filtre == 3:
            imgX, imgY, imgN = filtres.filtreSobel(img)
            img2 = img + alpha * (imgX + imgY)
        elif filtre == 4:
            imgX, imgY, imgN = filtres.filtreRoberts(img)
            img2 = img + alpha * (imgX + imgY)
        elif filtre == 5:
            img2 = filtres.filtreLaplacien(img, noyau)
        elif filtre == 6:
            img2 = filtres.filtreLaplacienRehausseur(img, alpha, noyau)
        
        # afficher l'image
        plt.figure(num_fig)
        num_fig += 1
        axes = plt.gca()
        axes.set_title("Image filtrée - " + nom_filtre)

        axes.imshow(img2, vmin = 0, vmax = 255, cmap='gray')
        #plt.imsave("img_filtree.png", img2, vmin = 0, vmax = 255, cmap='gray')

        # si sobel ou roberts, afficher imgX et imgY
        if filtre == 3 or filtre == 4:
            fig = plt.figure(num_fig)
            num_fig += 1
            
            ax1, ax2, ax3 = fig.subplots(1, 3, sharey=True)
            ax1.imshow(imgX, cmap='gray')
            ax1.set_title('Filtrage en X')
            ax2.imshow(imgY, cmap='gray')
            ax2.set_title('Filtrage en Y')
            ax3.imshow(imgN, cmap='gray')
            ax3.set_title('Norme 2 du filtrage en X et Y')
            fig.suptitle("Etapes de filtrage de l'image originale")
        
        
        # si on doit afficher une ligne
        if draw_line_signal != -1:
            fig = plt.figure(num_fig)
            num_fig += 1
            
            t = np.arange(img.shape[1])
            x = img[draw_line_signal]
            y = img2[draw_line_signal]
            
            plt.plot(t, x, label="signal original")
            plt.plot(t, y, label="signal filtré")
            plt.title("Signal de la ligne "+str(draw_line_signal)+" de l'image avant et après filtrage")
            plt.legend(loc="best")


    plt.show()
