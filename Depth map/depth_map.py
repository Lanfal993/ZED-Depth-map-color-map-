########################################################################
#
# Copyright (c) 2023, ZQ Photoelectrics
#
# All rights reserved.
#
########################################################################

#Todo: Borrar
#----------------------#
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import ctypes
import sys
import math
from threading import Lock
import numpy as np
import array
#----------------------#
import sys
import pyzed.sl as sl
import ogl_viewer.viewer as gl

#Init#
if __name__ == "__main__":
    print("Running Depth Sensing sample ... Press 'Esc' to quit")

    init = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,
                                 depth_mode=sl.DEPTH_MODE.ULTRA,
                                 coordinate_units=sl.UNIT.METER,
                                 coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)
    zed = sl.Camera()
    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    res = sl.Resolution()
    res.width = 720
    res.height = 404

    camera_model = zed.get_camera_information().camera_model
    # Create OpenGL viewer
    viewer = gl.GLViewer()
    viewer.init(len(sys.argv), sys.argv, camera_model, res)
    #==================================================================================#
    # Create OpenGL viewer
    #==================================================================================#
    #Todo: Esto se tiene que mandar a un folder aparte.




    #==================================================================================#
    #Camera Loop#
    #==================================================================================#
    while viewer.is_available():
        if zed.grab() == sl.ERROR_CODE.SUCCESS: # It means that it connected to the camera succesfully
            print("Connected...")

        else:
            print("Problem with the camera connection...")
            

    
    # zed.close()
    #==================================================================================#