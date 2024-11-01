import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
homeX, homeY, homeZ = 170, 0, 50
ctrlDobot = dbt.DoBotArm("COM3", homeX, homeY, homeZ, home= False)
print("starting")

ctrlDobot.moveHome() #this needs to be here for some reason
ctrlDobot.moveArmXYZ(x= 170, y= 50, z= 0)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)

time.sleep(2)
ctrlDobot.moveArmRelXYZ(0,0,40)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= -7)

ctrlDobot.toggleSuction()
time.sleep(5)
ctrlDobot.moveArmRelXYZ(0,0,40)
time.sleep(5)
ctrlDobot.toggleSuction()
ctrlDobot.SetConveyor(True, 15000)
time.sleep(5)
ctrlDobot.SetConveyor(True, 0)
#def SetConveyor(self, enabled, speed = 15000):


