

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

    def go_to_pos():# no Z movement

       # x = circle1.pixel_pos.x * ratio
       # y = circle1.pixel_pos.y * ratio
    
       # Dobot.movearm(z, y, z)

        return None

    def get_current_pos():
        pass
    
    def get_desired_pos():
        placeholder = 0
        return placeholder #TODO:

    def pick():# platform + object z
        #toggle end effector
        return None

    def place():#conveyor z
        return None

    def get_ratio(): #to call once in init
        # Move arm to camera view
        # while arm not detected
        # move arm x or y by a bit, get-pos
        # once detected get pixel_pos
        # move arm x,y by n-amount, get-pos
        # get pixel pos
        # ratio = pixel_pos-pixelpos0/ get_pos - get_pos0

        return ratio

    def convert_to_