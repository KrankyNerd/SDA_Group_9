
import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType # because conveyor is connected and controlled by dobot
class Conveyor:
    def __init__(self, velocity):
        self.velocity = velocity
        
    
    def move_conveyor(self,enabled,velocity):
        dType.SetEMotor(self.api, 0, enabled, velocity)
        return None
        