# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:27:24 2023

@author: alexander
"""



import numpy as np
from PIL import Image
import matplotlib.pyplot as plt




# Load the .npy file
data = np.load("depth_prueba.npy")

# Create a PIL image from the NumPy array
img = Image.fromarray(data)

# Show the image in a window
plt.imshow(img)

plt.show()


