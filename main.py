"""main function that controls the loading cycle"""

# 1import libraries and classes
import threading
import DoBotArm as dbt
import DobotDllType as dType
import time
import numpy as np
from serial.tools import list_ports
import cv2
from typing import List, Tuple
from Camera import Camera
from GUI import GUI
from types import MethodType # Monkey patch the function to the object

# constants 
homeX, homeY, homeZ = 170, 0, 30
homeX, homeY, homeZ = 170, 0, 30


#global variables
selected_shape = {"x": None, "y": None}  # Store shape coordinates globally

# objects
myCamera = Camera(address=1)
myGUI = GUI(resolution=(640, 480), duration=500, product_list=[], product_selection=True)
ctrlDobot = dbt.DoBotArm(
    "COM5", homeX, homeY, homeZ, home=False
)

# -----------------------methods-------------------------

def toggleSuction(self, state, wait=True):
    """
    Toggles the suction cup ON/OFF.
    :param state: True to turn suction ON, False to turn it OFF
    :param wait: If True, waits for execution
    """
    self.suction = state  # Update suction state variable
    self.lastIndex = dbt.dType.SetEndEffectorSuctionCup(
        self.api, 1, 1 if state else 0, isQueued=1
    )[0]

    if wait:
        self.commandDelay(self.lastIndex)
    return self.lastIndex

def handle_mouse_click(event, x, y, flags, param):
    print("Mouse clicked")  # Debugging
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse Click at ({x}, {y})")  # Debugging
        for shape in detected_shapesdata:
            print(f"Checking shape at ({shape['pixel_posx']}, {shape['pixel_posy']})")  # Debugging
            if (
                abs(x - shape["pixel_posx"]) < 10
                and abs(y - shape["pixel_posy"]) < 10
            ):
                print(f"Clicked on {shape['product_type']} at ({x}, {y})!")
                selected_shape["x"] = shape["pixel_posx"]
                selected_shape["y"] = shape["pixel_posy"]
                print("Shape Selected:", selected_shape)  # Debugging
                break


# --------------- end of methods -------------------------



#-------------------initialization-------------------
print("starting!")
ctrlDobot.toggleSuction = MethodType(toggleSuction, ctrlDobot)
cv2.namedWindow("Processed Image")
cv2.setMouseCallback("Processed Image", handle_mouse_click)
# ------------------------------------------------

#-------------------main flow---------------

ctrlDobot.moveHome()  # README: this assumes the arm is initialized in DOBOTLAB with home position (170, 0, 30)
ctrlDobot.moveArmXYZ(None, -200, 30) #arm gets out of camera fov
time.sleep(1)
myCamera.run()

while True:
    frame = myCamera.get_image()
    if frame is not None:
        processed_image, detected_shapesdata, _ = myCamera.process_image(frame)
        cv2.imshow("Processed Image", processed_image)

        # Ensure OpenCV is processing events
        cv2.waitKey(1)

        # Debugging: Print detected shapes
        print("Detected Shapes Data:", detected_shapesdata)

        # Check if shape has been selected
        if selected_shape["x"] is not None and selected_shape["y"] is not None:
            break  # Exit loop once a shape is selected

dobot_x = 0.71 * selected_shape["x"] + 124
dobot_y = -0.738 * selected_shape["y"] + 99.76
    
   
ctrlDobot.moveArmXYZ(dobot_x, dobot_y, 30)
ctrlDobot.moveArmXYZ(dobot_x, dobot_y, -34.0)
time.sleep(2)
ctrlDobot.toggleSuction(True)
ctrlDobot.moveArmXYZ(None, None, 30)
ctrlDobot.moveHome()
ctrlDobot.moveArmXYZ(None, -220, 30)
ctrlDobot.moveArmXYZ(100, -220, 30)
time.sleep(2)
ctrlDobot.toggleSuction(False)
ctrlDobot.moveArmXYZ(170, -220, 30)
ctrlDobot.moveArmXYZ(None, -220, 30)
ctrlDobot.moveHome()

# Break the loop on 'q' key press
if cv2.waitKey(1) & 0xFF == ord("q"):
    myCamera.release()