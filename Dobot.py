
import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType
import time


"""-------The DoBot Control Class-------
Variables:
suction = Suction is currently on/off
picking: shows if the dobot is currently picking or dropping an item
api = variable for accessing the dobot .dll functions
home% = home position for %
                                  """CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
}
class Dobot:
    def __init__(self, current_pos, current_x, current_y, current_z, desired_pos, desired_x, desired_y, desired_z, home_pos, error, moving_x, moving_y, moving_z, end_pos, dobot_serial_timeout):
        self.current_pos = current_pos
        self.current_x = current_x
        self.current_y = current_y
        self.current_z = current_z
        self.desired_pos = desired_pos
        self.desired_x = desired_x
        self.desired_y = desired_y
        self.desired_z = desired_z
        self.home_pos = home_pos
        self.error = error
        self.moving_x = moving_x
        self.moving_y = moving_y
        self.moving_z = moving_z
        self.end_pos = end_pos
        self.dobot_serial_timeout = dobot_serial_timeout
        self.api = dType.load()#to access the library containing our dll functions
        self.rotation = 0
        self.connected = False
        self.home_time = 0
        self.dobotConnect(home, homingWait)
        self.lastIndex = 0
        self.rotation = self.getPosition()[3]


    def go_to_pos():
        return None

    def get_curren_pos():
        placeholder = 0
        return dType.GetPose(self.api)
        return placeholder #TODO:

    def get_desired_pos():
        placeholder = 0
        return placeholder #TODO:

    def pick():
        return None

    def place():
        return None
