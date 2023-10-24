# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:27:24 2023

@author: alexander
"""



import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2



# Load the .npy file
data = np.load("depth_me.npy")

    
# Create a PIL image from the NumPy array
depth_image = Image.fromarray(data)

# Show the image in a window
plt.imshow(depth_image)

# Verificar si la carga fue exitosa
if depth_image is not None:
    # Normalizar la imagen de profundidad para que esté en el rango [0, 255]
    normalized_depth_image = ((depth_image - np.min(depth_image)) / (np.max(depth_image) - np.min(depth_image)) * 255).astype(np.uint8)

    # Convertir la imagen normalizada a escala de grises
    grayscale_image = cv2.cvtColor(normalized_depth_image, cv2.COLOR_GRAY2BGR)

    # Guardar la imagen en escala de grises si es necesario
    #cv2.imwrite('imagen_en_escala_de_grises.png', grayscale_image)

    # Mostrar la imagen en escala de grises en una ventana (opcional)
    #cv2.imshow('Imagen en Escala de Grises', grayscale_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No se pudo cargar la imagen de profundidad en formato .npy.")


