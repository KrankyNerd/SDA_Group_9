import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
homeX, homeY, homeZ = 170, 0, 0
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)
#ctrlDobot.rehome(homeX, homeY, )


#print("starting")
#ctrlDobot.moveArmXYZ(x= 100, y= 0, z= 0)
ctrlDobot.moveHome()
print("movement finshed")
#ctrlDobot.moveArmRelXYZ(x = 170, y= 50 , z = 30)
# def SetConveyor(self, enabled, speed = 15000):



