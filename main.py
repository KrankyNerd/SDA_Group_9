

"""main function, that controls the loading cycle"""
#1import libraries and classes
import threading
import DoBotArm as dbt
import time
import Conveyor
import Camera
import GUI
import Dobot
import EndEffector
#from serial.tools import list_ports


#2 define constants
homeX, homeY, homeZ = 170, 0, 0


#3 Create objects of the needed classes
conveyor= Conveyor(True,0)
camera = Camera(address=2)
end_effector = EndEffector (False)
myGUI=GUI(0, 5000,[],False)# resolution, timer duration, product list, product selection
ctrlDobot = dbt.DoBotArm("COM3", homeX, homeY, homeZ, home= False)# dobot or DobotArm?? Isa

 #Dobot starts at home
print("starting")

ctrlDobot.moveHome() #this needs to be here for some reason
ctrlDobot.moveArmXYZ(x= 170, y= 50, z= 0)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= 0)
time.sleep(2)
#4 Camera setup and  Camera image detection
camera.run()

#5a GUI display 
myGUI.display_products()
#5b User input handling
# 6 Moving product

#6a obtain product position and move to it

# 6b pick product :lower arm, toggle end effector, raise arm
ctrlDobot.moveArmRelXYZ(0,0,40)
ctrlDobot.moveArmXYZ(x= 170, y= 0, z= -7)
ctrlDobot.toggleSuction()
time.sleep(5)
# 6 c move to conveyor position, lower arm, toggle end effector, raise arm
ctrlDobot.moveArmRelXYZ(0,0,40)
time.sleep(5)
ctrlDobot.toggleSuction()

# 6d home dobot, move conveyor, stop conveyor
##conveyor.move_conveyor(True, 15000)#start conveyor
time.sleep(5)#delay
#conveyor.move_conveyor(True, 0)#stops conveyor
camera.release()

# ctrlDobot.SetConveyor(True, 15000)#start conveyor
# time.sleep(5)#delay
# ctrlDobot.SetConveyor(True, 0)#stops conveyor
# #def SetConveyor(self, enabled, speed = 15000):


