# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:48:26 2023

@author: alexander
"""



import configuracion as conf      #Importo el archivo de configuracion 
import captura_frame as frame       #importo el archivo de capture_frame para acceder a las funciones 


#trigger_mode=1, deep_mode=1, deep_shift=255, ir_mode=1, status_mode=2, status_mask=7, rgb_mode=1, rgb_res=0, expose_time=0

if frame.post_encode_config(conf.frame_config_encode(1,1,255,1,2,7,1,0,0)):
    p = frame.get_frame_from_http()
    profundidad, ir, status, rgb = frame.show_frame(p)
    # with open("rgbd.raw", 'wb') as f:
    #     f.write(p)
    #     f.flush()



