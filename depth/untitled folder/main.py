from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk
import cv2 as cv
import pyzed.sl as sl

zed = sl.Camera()

class App:
    def __init__(self, root):
        self.root = root
        # Create a Camera object
        

        # Create a InitParameters object and set configuration parameters
        init_params = sl.InitParameters()
        init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
        init_params.camera_fps = 15  # Set fps at 15

        # Open the camera
        err = zed.open(init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            exit(1)

        # Screen size
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # Color pallete options
        colors = ['白黑','彩虹', '彩色','红蓝', '铁红']

        # Initialize click coordinates and distance value
        self.click_x = 0
        self.click_y = 0
        self.value = float(1.0)

        # Declare measurement array
        self.array_measure = []

        # NOTE: OPTIONS: Setting variable for Integers 
        self.variable = StringVar()
        self.variable.set(colors[4])

        # Create frame to place a grid
        self.f1 = Frame(master=root)
        self.f1.pack(fill="both", expand=True)

        # Configure grid
        self.f1.columnconfigure(0, weight=1)
        self.f1.columnconfigure(1, weight=1)

        self.f1.rowconfigure(0, weight=1)

        # Create a label and display it on app
        self.label_widget = Label(self.f1)
        self.label_widget.grid(column=0, row=0)
        self.label_widget.bind("<ButtonPress-1>", self.OnMouseDown)
        
        frame_right = Frame(self.f1)
        frame_right.grid(column=1,row=0)

        # Create a label to display distance
        self.label_distance = Label(self.frame_right)
        self.label_distance.pack()

        # Option menu
        dropdown = OptionMenu(frame_right,self.variable,*colors)
        dropdown.pack()

        #Start getting frames from the camera
        self.get_frames()


    def OnMouseDown(self, event):
        self.click_x = event.x
        self.fclick_y = event.y
        print("frame coordinates: {0}/{1}".format(event.x, event.y))
        self.get_value()

    
    def get_value(self):
        if len(self.array_measure) <= 1:
            self.array_measure.append(self.value)
        if len(self.array_measure) == 1:


    def get_frames(self):
        runtime_parameters = sl.RuntimeParameters()
        runtime_parameters.enable_fill_mode = True

        # Video resolution  according to video stream NOTE: (HD1080)
        x = 1920 
        y = 1080 

        # Create an RGBA sl.Mat object
        image_depth_zed = sl.Mat(x, y, sl.MAT_TYPE.U8_C4)

        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS :

            # Retrieve the normalized depth image
            zed.retrieve_image(image_depth_zed, sl.VIEW.DEPTH)

            # Get the distance value of the give coordinate
            self.value = image_depth_zed.get_value(self.click_x, self.click_y,memory_type = sl.MEM.CPU)

            # Use get_data() to get the numpy array
            image_depth_ocv = image_depth_zed.get_data()

            # Normalize image
            gray = cv.cvtColor(image_depth_ocv, cv.COLOR_BGR2GRAY)

            # Color pallete options
            if self.variable.get() == '彩虹':
                gray = cv.applyColorMap(gray, cv.COLORMAP_RAINBOW)

            if self.variable.get() == '红蓝':
                gray = cv.applyColorMap(gray, cv.COLORMAP_JET)

            if self.variable.get() == '彩色':
                gray = cv.applyColorMap(gray, cv.COLORMAP_HSV)

            if self.variable.get() == '铁红':
                gray = cv.applyColorMap(gray, cv.COLORMAP_HOT)

            # Resize image
            resized = cv.resize(gray, dsize=(int(self.screen_width/2), int(self.screen_height/2)), interpolation=cv.INTER_CUBIC)

            # Convert captured image to photoimage
            photo_image = ImageTk.PhotoImage(image=Image.fromarray(resized))

            # Displaying photoimage in the label
            self.label_widget.photo_image = photo_image

            # Configure image in the label
            self.label_widget.configure(image=photo_image)

            # Repeat the same process after every 10 seconds
            self.label_widget.after(10, self.get_frames)


# Create an infinite loop for displaying app on screen
root = Tk()
app = App(root)
root.mainloop()