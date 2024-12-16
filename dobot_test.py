import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
homeX, homeY, homeZ = 170, 0, 50
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)
print("starting")
ctrlDobot.moveHome()

ctrlDobot.moveArmXYZ(x= 170, y= 50, z= 0)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)


ctrlDobot.moveArmRelXYZ(0,0,30)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)

ctrlDobot.toggleSuction()
time.sleep(10)
ctrlDobot.toggleSuction()

ctrlDobot.moveHome()
#def SetConveyor(self, enabled, speed = 15000)