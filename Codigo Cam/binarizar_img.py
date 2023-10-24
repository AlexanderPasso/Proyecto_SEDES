# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:12:19 2023

@author: alexa
"""

import cv2

# Cargar la imagen en escala de grises
gray_image = cv2.imread('imagen_en_escala_de_grises.png', cv2.IMREAD_GRAYSCALE)

# Aplicar umbralización
umbral, imagen_binarizada = cv2.threshold(gray_image, 118, 255, cv2.THRESH_BINARY)

#Guardar imagen
#cv2.imwrite('imagen_binarizada.png', imagen_binarizada)


# Mostrar la imagen binarizada
cv2.imshow('Imagen binarizada', imagen_binarizada)
cv2.waitKey(0)
cv2.destroyAllWindows()