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
    
    # Condition to continue
    while True:
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.DEPTH)
            image_ocv = image.get_data()
            # Normalize image
            gray = cv.cvtColor(image_ocv, cv.COLOR_BGR2GRAY)
            # Color pallete "JET"
            jet = cv.applyColorMap(gray, cv.COLORMAP_JET)
            cv.imshow("JET", jet)

            # cv.imwrite("images.png", image_ocv)

            # 
            # cv.imwrite("grey.png", gray)

            # autum = cv.applyColorMap(gray, cv.COLORMAP_AUTUMN)
            # cv.imwrite("autum.png", autum)

            # hsv = cv.applyColorMap(gray, cv.COLORMAP_HSV)
            # cv.imwrite("hsv.png", hsv)

            # hot = cv.applyColorMap(gray, cv.COLORMAP_HOT)
            # cv.imwrite("hot.png", hot)

       
            
            

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()