"""testing moving the arm and changing coordinates with pixel to meter ratio, not with matrix transformation"""

#import libraries and classes
import DoBotArm as dbt
import time
import numpy as np
import cv2
from serial.tools import list_ports
from Camera import Camera

#constants
homeX, homeY, homeZ = 170, 0, 30
xpixel_to_cm = 16/219
ypixel_to_cm = 16/227
cm_to_dobot_x = 128/12.5
cm_to_dobot_y = -133/12.5
#conveyorPos = 20, -220, 30

#objects
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)
myCamera = Camera(address=1)

#-----------------------methods-------------------------

#--------------- end of methods -------------------------

# ------------------- MAIN   START -------------------------

ctrlDobot.moveHome()
time.sleep(1)
print("homing finished")

#the base is 220px x 220px
#and 0.16m x 0.16m
# 0r 12.5cm x 12.5cm if you consider the center of the products

# arm get out of camera pov
print("arm go away")
ctrlDobot.moveArmXYZ(None, -200, 30)
time.sleep(2)
ctrlDobot.moveArmXYZ(80, -200, 30)
time.sleep(2)

#run camera
print("camera go flash")
myCamera.run()
time.sleep(2)

detected_shapesdata = myCamera.run() 

if detected_shapesdata:
    for shape in detected_shapesdata:
        positions = [(shape['pixel_posx']*xpixel_to_cm, shape['pixel_posy']*ypixel_to_cm) for shape in detected_shapesdata]
else:
    print("No shapes detected.")


ctrlDobot.moveHome()
time.sleep(2)
print("Yes")

ctrlDobot.moveArmXYZ(138, -48, 30)
print("Position 1")

for x, y in positions:
    dobot_x = 138 + x*cm_to_dobot_x
    dobot_y = -48 + y*cm_to_dobot_y
    ctrlDobot.moveArmXYZ(dobot_x, dobot_y, 30)
    print(dobot_x)
    print(dobot_y)
    time.sleep(2)

#ctrlDobot.DisconnectDobot()