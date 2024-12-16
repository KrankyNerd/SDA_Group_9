import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
homeX, homeY, homeZ = 170, 0, 30
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)
#ctrlDobot.rehome(homeX, homeY, )


#print("starting")
#ctrlDobot.moveArmXYZ(x= 170, y= -100, z= 40)
ctrlDobot.moveHome()
print("movement finshed")
time.sleep(5)
ctrlDobot.moveArmXYZ(170, -100 , 40)
print("YEs")
ctrlDobot.DisconnectDobot()
# def SetConveyor(self, enabled, speed = 15000):



