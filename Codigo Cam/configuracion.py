# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:46:05 2023

@author: alexander
"""

import struct
import numpy as np
import cv2


def frame_config_decode(frame_config):
    '''
        @frame_config bytes

        @return fields, tuple (trigger_mode, deep_mode, deep_shift, ir_mode, status_mode, status_mask, rgb_mode, rgb_res, expose_time)
    '''
    return struct.unpack("<BBBBBBBBi", frame_config)


def frame_config_encode(trigger_mode=1, deep_mode=1, deep_shift=255, ir_mode=1, status_mode=2, status_mask=7, rgb_mode=1, rgb_res=0, expose_time=0):
    '''
        @trigger_mode, deep_mode, deep_shift, ir_mode, status_mode, status_mask, rgb_mode, rgb_res, expose_time

        @return frame_config bytes
    '''
    return struct.pack("<BBBBBBBBi",
                       trigger_mode, deep_mode, deep_shift, ir_mode, status_mode, status_mask, rgb_mode, rgb_res, expose_time)


def frame_payload_decode(frame_data: bytes, with_config: tuple):
    '''
        @frame_data, bytes

        @with_config, tuple (trigger_mode, deep_mode, deep_shift, ir_mode, status_mode, status_mask, rgb_mode, rgb_res, expose_time)

        @return imgs, tuple (deepth_img, ir_img, status_img, rgb_img)
    '''
    deep_data_size, rgb_data_size = struct.unpack("<ii", frame_data[:8])
    frame_payload = frame_data[8:]
    # 0:16bit 1:8bit, resolution: 320*240
    deepth_size = (320*240*2) >> with_config[1]
    deepth_img = struct.unpack("<%us" % deepth_size, frame_payload[:deepth_size])[
        0] if 0 != deepth_size else None
    frame_payload = frame_payload[deepth_size:]

    # 0:16bit 1:8bit, resolution: 320*240
    ir_size = (320*240*2) >> with_config[3]
    ir_img = struct.unpack("<%us" % ir_size, frame_payload[:ir_size])[
        0] if 0 != ir_size else None
    frame_payload = frame_payload[ir_size:]

    status_size = (320*240//8) * (16 if 0 == with_config[4] else
                                  2 if 1 == with_config[4] else 8 if 2 == with_config[4] else 1)
    status_img = struct.unpack("<%us" % status_size, frame_payload[:status_size])[
        0] if 0 != status_size else None
    frame_payload = frame_payload[status_size:]

    assert(deep_data_size == deepth_size+ir_size+status_size)

    rgb_size = len(frame_payload)
    assert(rgb_data_size == rgb_size)
    rgb_img = struct.unpack("<%us" % rgb_size, frame_payload[:rgb_size])[
        0] if 0 != rgb_size else None

    if (not rgb_img is None):
        if (1 == with_config[6]):
            jpeg = cv2.imdecode(np.frombuffer(
                rgb_img, 'uint8', rgb_size), cv2.IMREAD_COLOR)
            if not jpeg is None:
                rgb = cv2.cvtColor(jpeg, cv2.COLOR_BGR2RGB)
                rgb_img = rgb.tobytes()
            else:
                rgb_img = None
        # elif 0 == with_config[6]:
        #     yuv = np.frombuffer(rgb_img, 'uint8', rgb_size)
        #     print(len(yuv))
        #     if not yuv is None:
        #         rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV420P2RGB)
        #         rgb_img = rgb.tobytes()
        #     else:
        #         rgb_img = None

    return (deepth_img, ir_img, status_img, rgb_img)