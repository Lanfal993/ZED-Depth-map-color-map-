import pyzed.sl as sl
import cv2 as cv
import numpy as np
import colorsys
from PIL import Image


def convert_to_hexa(value):

    # NOTE: The color pallete is 0-255 in HSV value
    (h, s, v) = (value, 1, 1)
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    print("Converted: {0} , {1}, {2}".format(r, g, b))        
    return r

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.camera_fps = 15  # Set fps at 15

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    image = sl.Mat()
    depth_map = sl.Mat()
    point_cloud = sl.Mat()

    image_zed = sl.Mat()

    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.enable_fill_mode = True

    # Screen size
    x = 1920 
    y = 1080 

    while True:
        # Create an RGBA sl.Mat object
        image_depth_zed = sl.Mat(x, y, sl.MAT_TYPE.U8_C4)

        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS :

            
            # Retrieve the normalized depth image
            zed.retrieve_image(image_depth_zed, sl.VIEW.DEPTH)
            # Use get_data() to get the numpy array
            image_depth_ocv = image_depth_zed.get_data()
            # Display the depth view from the numpy array
            
            value = image_depth_zed.get_value(10,10,memory_type = sl.MEM.CPU)
            print("REAL TIME VALUE 10x10 : {0}".format(value))

             # Normalize image
            gray = cv.cvtColor(image_depth_ocv, cv.COLOR_BGR2GRAY)
            # Color pallete "JET"
            jet = cv.applyColorMap(gray, cv.COLORMAP_JET)

            cv.imshow("Image", image_depth_ocv)
            if cv.waitKey(30) >= 0 :
                break

            
            

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()