"""testing moving the arm and changing coordinates with pixel to meter ratio, not with matrix transformation"""

# import libraries and classes
import DobotDllType as dType
import DoBotArm as dbt
import time
import numpy as np
import cv2
from serial.tools import list_ports
from Camera import Camera
from GUI import *
import threading


# constants
homeX, homeY, homeZ = 170, 0, 30
pixel_to_cm = 1 / 14.4
cm_to_dobot = 10.528
# conveyorPos = 20, -220, 30

# objects
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home=False)
myCamera = Camera(address=1)
myGUI = GUI(resolution=(640, 480), duration=500, product_list=[], product_selection=True)

# -----------------------methods-------------------------


# Define the function outside the class
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


# Monkey patch the function to the object
from types import MethodType

ctrlDobot.toggleSuction = MethodType(toggleSuction, ctrlDobot)

# --------------- end of methods -------------------------


# ------------------- MAIN   START -------------------------

ctrlDobot.SetConveyor(enabled=1, speed= 15000)
time.sleep(3)
ctrlDobot.SetConveyor(enabled=1, speed=-15000)
time.sleep(3)
ctrlDobot.SetConveyor(enabled=0)

selected_shape = {"x": None, "y": None}  # Store shape coordinates globally

# Debugging: Make sure OpenCV recognizes clicks
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

# Create OpenCV window and set mouse callback
cv2.namedWindow("Processed Image")
cv2.setMouseCallback("Processed Image", handle_mouse_click)

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
print(f"Dobot Coordinates: X={dobot_x}, Y={dobot_y}")

"""
while True:
    frame = myCamera.get_image()
    if frame is not None:
        processed_image, detected_shapesdata, _ = myCamera.process_image(frame)

        # Display the processed image
        cv2.imshow("Processed Image", processed_image)
        # Instantiate and display detected products
        myGUI.instantiate_product(detected_shapesdata)
        cv2.waitKey(1) 
        # myGUI.display_products()
        # Mouse interaction for shape clicks
        def handle_mouse_click(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                print("Mouse clicked")
                for shape in detected_shapesdata:
                    if (
                        abs(x - shape["pixel_posx"]) < 10
                        and abs(y - shape["pixel_posy"]) < 10
                    ):
                        print(f"Clicked on {shape['product_type']} at ({x}, {y})!")
                        selected_shape = [shape["pixel_posx"], shape["pixel_posy"]]
                        print(selected_shape)
                        break
        cv2.setMouseCallback("Processed Image", handle_mouse_click)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        myCamera.release()
        break



ctrlDobot.moveHome()
time.sleep(1)
print("homing finished")

#the base is 220px x 220px
#and 0.16m x 0.16m

# arm get out of camera pov
print("arm go away")
ctrlDobot.moveArmXYZ(None, -200, 30)
time.sleep(1)

#run camera
print("camera go flash")
myCamera.run()
time.sleep(1)

detected_shapesdata = myCamera.run() 

# change this to get positions in centimeters (CONVERT)
if detected_shapesdata:
    for shape in detected_shapesdata:
        positions = [(shape['pixel_posx'], shape['pixel_posy']) for shape in detected_shapesdata]
else:
    print("No shapes detected.")

#for every shape, dobot coordinate =  position (x.y) in cm * 10.528
ctrlDobot.moveArmXYZ(138.4, -63.8, 30)

for x, y in positions:
    dobot_x = 0.71 * x + 124
    dobot_y = -0.738 * y + 99.76
    ctrlDobot.moveArmXYZ(dobot_x, dobot_y, 30)
    ctrlDobot.moveArmXYZ(dobot_x, dobot_y, -34.0)
    #ctrlDobot.toggleSuction()
    #ctrlDobot.pickToggle(-31.5, True)
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

    print("camera coordinates:")
    print(x, y)
    
    print("dobot coordinates:")
    print(dobot_x, dobot_y)

    time.sleep(2)

#ctrlDobot.DisconnectDobot()""""