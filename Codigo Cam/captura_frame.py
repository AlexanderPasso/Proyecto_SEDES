# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:49:31 2023

@author: alexander
"""

import numpy as np
import matplotlib.pyplot as plt
import struct
import requests
import configuracion as conf      #Importo el archivo de configuracion 
from PIL import Image
import cv2


HOST = '192.168.233.1'
PORT = 80

def post_encode_config(config=conf.frame_config_encode(),host=HOST, port=PORT):
    r = requests.post('http://{}:{}/set_cfg'.format(host, port), config)
    if(r.status_code == requests.codes.ok):
        return True
    return False

def post_CameraParmsBytes(cameraParms:bytes,host=HOST, port=PORT):
    r = requests.post('http://{}:{}/calibration'.format(host, port), cameraParms)
    if(r.status_code == requests.codes.ok):
        print("ok")

def get_frame_from_http(host=HOST, port=PORT):
    r = requests.get('http://{}:{}/getdeep'.format(host, port))
    if(r.status_code == requests.codes.ok):
        print('Get deep image')
        deepimg = r.content
        print('Length={}'.format(len(deepimg)))
        (frameid, stamp_msec) = struct.unpack('<QQ', deepimg[0:8+8])
        print((frameid, stamp_msec/1000))
        return deepimg


def show_frame(frame_data: bytes):
    config = conf.frame_config_decode(frame_data[16:16+12])
    frame_bytes = conf.frame_payload_decode(frame_data[16+12:], config)

    depth = np.frombuffer(frame_bytes[0], 'uint16' if 0 == config[1] else 'uint8').reshape(
        240, 320) if frame_bytes[0] else None

    ir = np.frombuffer(frame_bytes[1], 'uint16' if 0 == config[3] else 'uint8').reshape(
        240, 320) if frame_bytes[1] else None

    status = np.frombuffer(frame_bytes[2], 'uint16' if 0 == config[4] else 'uint8').reshape(
        240, 320) if frame_bytes[2] else None

    rgb = np.frombuffer(frame_bytes[3], 'uint8').reshape(
        (480, 640, 3) if config[6] == 1 else (600, 800, 3)) if frame_bytes[3] else None
    
    
    #Medir distancia al centro de la imagen
    center_dist = depth[240//2, 320//2]
    if 0 == config[1]:
       #print("%f mm" % (center_dist/4))
       center_dist = center_dist/4
    else:
       #print("%f mm" % ((center_dist/5.1) ** 2))
       center_dist = (center_dist/5.1) ** 2

    figsize = (12, 12)
    fig = plt.figure(figsize=figsize)

    ax1 = fig.add_subplot(221)
    if not depth is None:
        ax1.imshow(depth)
        #np.save("depth_me.npy", depth)
        # np.savetxt("depth.csv", (depth/4).astype('uint16'), delimiter="," )
    ax2 = fig.add_subplot(222)
    if not ir is None:
        ax2.imshow(ir)
   

    ax3 = fig.add_subplot(223)
    if not status is None:
        ax3.imshow(status)
    ax4 = fig.add_subplot(224)
    if not rgb is None:
        ax4.imshow(rgb)
        # Create a PIL image from the NumPy array
        img = Image.fromarray(rgb)

        # Save the image to a file
        #img.save("prueba_me.jpg")
    return depth, rgb, center_dist