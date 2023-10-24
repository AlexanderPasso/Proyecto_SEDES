# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 11:57:11 2023

@author: alexa
"""


import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import open3d as o3d
import captura_frame as frame

# Load the .npy file
depth_image = np.load('depth_prueba.npy')



# print properties:
print(f"Image resolution: {depth_image.shape}")
print(f"Data type: {depth_image.dtype}")
print(f"Min value: {np.min(depth_image)}")
print(f"Max value: {np.max(depth_image)}")



