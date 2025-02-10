# Traitement_images

## TP1

Commandes lancées pour obtenir les images du dossier resultat :

```
python3 rgb_stretching.py data/foret.png -C -S -H
python3 rgb_stretching.py data/foret.png -C -S -H -e 0 130

python3 ycbcr_stretching.py data/foret.png -C -S -H

python3 hsv_stretching.py data/foret.png -C -S -H -v
python3 hsv_stretching.py data/foret.png -C -S -H -h -e 0 130
python3 hsv_stretching.py data/foret.png -C -H -S -H -s -e 100 250
python3 hsv_stretching.py data/foret.png -C -H -S -H -v -e 0 130
```

Pour le fun faire de même avec l'orque (enlever -H pour ne pas avoir les histogrammes, enlever -C pour ne pas avoir les trois canaux en niveau de gris)