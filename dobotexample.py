"""main function, that controls the loading cycle"""
#1import libraries and classes
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
time.sleep(1)
ctrlDobot.moveArmXYZ(220, -60, 30)
ctrlDobot.moveArmXYZ(220, 50, 30)
ctrlDobot.moveArmXYZ(150, 50, 30)
ctrlDobot.moveArmXYZ(180, -60, 30)
#ctrlDobot.moveArmXYZ(20, -220, 30) #correct coordinates for conveyor

print("YEs")
ctrlDobot.DisconnectDobot()
# def SetConveyor(self, enabled, speed = 15000):



