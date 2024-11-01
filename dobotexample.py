"""main function, that controls the loading cycle"""
#1import libraries and classes
import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports


#2 define constants
homeX, homeY, homeZ = 170, 0, 0


#3 Create objects of the needed classes

ctrlDobot = dbt.DoBotArm("COM3", homeX, homeY, homeZ, home= False)

 #Dobot starts at home
print("starting")

ctrlDobot.moveHome() #this needs to be here for some reason
ctrlDobot.moveArmXYZ(x= 170, y= 50, z= 0)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)
time.sleep(2)
#4a Camera setup
#4b Cmera image detection
#5a GUI display 
#5b User input handling
# 6 Moving product
#6a obtain product position and move to it

# 6b pick product :lower arm, toggle end effector, raise arm

# 6 c move to conveyor position, lower arm, toggle end effector, raise arm
# 6d home dobot, move conveyor, stop conveyor



ctrlDobot.moveArmRelXYZ(0,0,40)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= -7)

ctrlDobot.toggleSuction()
time.sleep(5)
ctrlDobot.moveArmRelXYZ(0,0,40)
time.sleep(5)
ctrlDobot.toggleSuction()
ctrlDobot.SetConveyor(True, 15000)#start conveyor
time.sleep(5)#delay
ctrlDobot.SetConveyor(True, 0)#stops conveyor
#def SetConveyor(self, enabled, speed = 15000):


