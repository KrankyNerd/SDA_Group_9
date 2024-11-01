# importing numpy module
import numpy as np
import random

"""
Class Dobot:
Higher-level class to pick and place items with a Dobot.
"""

import DoBotArm


class Dobot(DoBotArm):
    def __init__(self, port, homeX, homeY, homeZ, home=False, homingWait=True):

        super().__init__(port, homeX, homeY, homeZ, home=False, homingWait=True)

        self.end_pos = ()
        self.home_pos = (self.homeX, self.homeY, self.homeZ)
        self.moving_z = 70.0 #height of product + height of conveyor 
        self.dobot_serial_timeout = False  # error variable

        self.moveHome  # move to home position at end of init

    def go_to_pos(self, x, y):  # no Z movement
        """
        Go to a (x, y) position. No movement in Z axis.

        :param:
        x: pixel position x coordinate
        y: pixel position y coordinate
        :return: None
        """


        np.array(list)

        self.moveArmXYZ(x, y, self.moving_z)

        return None

    def get_current_pos(self):
        # Unpack the first three values (x, y, z) directly from the list returned by getPosition
        x, y, z, *_ = self.getPosition()  # Ignore the rest of the values using "*_"
        return (x, y, z)  # Return the position as a tuple

    def pick(self):  # platform + object z

        # toggle end effector
        return None

    def place(self):  # conveyor z
        return None

    def manual_calibrate(self): #call once in init
        """
        Prompts the user to manually calibrate the dobot by recording 
        calibration points from both the camera and the robot.
        """

        try:
            num_points = int(input("How many points do you want to record?\n>>> "))
            
            for i in range(num_points):
                input("Place the robot arm somewhere in the FOV and press enter\n>>> ")
                
                camera.run()

                # Simulating camera and robot points
                camera_point = camera.detected_shapes[0]['coordinates']
                robot_point = self.get_current_pos()
                
                # Store the calibration point pair
                self.calibration_points.append((camera_point, robot_point))
                
                print(f"Point recorded - camera: {camera_point} robot: {robot_point}")
            
            print("\nPoints recorded, thank you!")
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")
