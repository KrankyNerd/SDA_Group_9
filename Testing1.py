"""testing moving the arm and changing coordinates with pixel to meter ratio, not with matrix transformation"""

#import libraries and classes
import DobotDllType as dType
import DoBotArm as dbt
import time
import numpy as np
import cv2
from serial.tools import list_ports
from Camera import Camera
import threading


#constants
homeX, homeY, homeZ = 170, 0, 30
pixel_to_cm = 1/14.4
cm_to_dobot = 10.528
#conveyorPos = 20, -220, 30

#objects
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)
myCamera = Camera(address=1)

#-----------------------methods-------------------------

# Define the function outside the class
def toggleSuction(self, state, wait=True):
    """
    Toggles the suction cup ON/OFF.
    :param state: True to turn suction ON, False to turn it OFF
    :param wait: If True, waits for execution
    """
    self.suction = state  # Update suction state variable
    self.lastIndex = dbt.dType.SetEndEffectorSuctionCup(self.api, 1, 1 if state else 0, isQueued=1)[0]
    
    if wait:
        self.commandDelay(self.lastIndex)
    return self.lastIndex

# Monkey patch the function to the object
from types import MethodType
ctrlDobot.toggleSuction = MethodType(toggleSuction, ctrlDobot)

#--------------- end of methods -------------------------


# ------------------- MAIN   START -------------------------

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

    print(dobot_x)
    print(dobot_y)
    time.sleep(2)

#ctrlDobot.DisconnectDobot()