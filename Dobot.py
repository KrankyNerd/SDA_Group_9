"""
Class Dobot:
Higher-level class to pick and place items with a Dobot.
"""

import DoBotArm


class Dobot(DoBotArm):
    def __init__(self, port, homeX, homeY, homeZ, home=False, homingWait=True):

        super().__init__(port, homeX, homeY, homeZ, home=False, homingWait=True)

        self.desired_pos = ()
        self.end_pos = ()
        self.home_pos = (self.homeX, self.homeY, self.homeZ)
        self.moving_z = 21.5  # not correct value: should be height of product + height of conveyor + a bit more
        self.dobot_serial_timeout = False  # error variable

        self.moveHome  # move to home position at end of init

    def go_to_pos(self):  # no Z movement
        """
        Go to a (x, y) position. No movement in Z axis.

        :return: None
        """

        # x = circle1.pixel_pos.x * ratio
        # y = circle1.pixel_pos.y * ratio

       # self.moveArmXYZ(x, y, self.moving_z)

        return None

    def get_current_pos(self):
        # Unpack the first three values (x, y, z) directly from the list returned by getPosition
        x, y, z, *_ = self.getPosition()  # Ignore the rest of the values using "*_"
        return (x, y, z)  # Return the position as a tuple

    def get_desired_pos(self):
        pass

    def pick(self):  # platform + object z
        # toggle end effector
        return None

    def place(self):  # conveyor z
        return None

    def get_ratio(self):  # to call once in init
        # Move arm to camera view
        # while arm not detected
        # move arm x or y by a bit, get-pos
        # once detected get pixel_pos
        # move arm x,y by n-amount, get-pos
        # get pixel pos
        # ratio = pixel_pos-pixelpos0/ get_pos - get_pos0
        ratio = float

        return ratio
