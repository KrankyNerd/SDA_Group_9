"""main function, that controls the loading cycle"""
#1import libraries and classes
import threading
import DoBotArm as dbt
import time
from serial.tools import list_ports
import Camera
homeX, homeY, homeZ = 170, 0, 30
ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)
#ctrlDobot.rehome(homeX, homeY, )

camera = Camera(address=1)



#print("starting")
#ctrlDobot.moveArmXYZ(x= 170, y= -100, z= 40)
ctrlDobot.moveHome()
print("movement finshed")
time.sleep(1)
#ctrlDobot.moveArmXYZ(175, -25, 20)
#ctrlDobot.moveArmXYZ(145, -20, 20)
#ctrlDobot.moveArmXYZ(160, 10, 20)
#ctrlDobot.moveArmXYZ(150, 0, 20)
#ctrlDobot.moveArmXYZ(20, -220, 30) #correct coordinates for conveyor

#ctrlDobot.DisconnectDobot()
# def SetConveyor(self, enabled, speed = 15000):

def get_sample_points(
    camera: Camera, dobot: Dobot
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Obtains a bunch of point samples expressed in both the given cameras' and dobots' frames of reference.
    """

    # README: this implementation currently is based on moving to a couple hardcoded points that *must always* be in the cameras' FOV. There are better options which require more time of implementation, such as having a human move the dobot arm with the keyboard and recording a bunch of points, or a "smart" program that can move the dobot in intervals until it exits the FOV

    # we need a minimum of 4 points to create a homography matrix
    # The more points and the more variation the better
    hardcoded_dobot_poses = [180
        (170, -25, 20),
        (145, -20, 20),
        (160, 10, 20),
        (150, 0, 20),
    ]  # TODO: find out good poses throught trial and error

    camera_coordinates_list = []
    dobots_coordinates_list = []

    for pose in hardcoded_dobot_poses:
        x, y, z = pose  # Unpack the x, y, z coordinates from the current pose
        dobot.moveArmXYZ(x, y, z)  # move arm
        camera_coordinates = dobot.getPosition() #get camera coordinates
        camera.run() # process image
        dobot_coordinates = camera.run() #TODO change to find_white_square() or whatever

        camera_coordinates_list.append(camera_coordinates)
        dobots_coordinates_list.append(dobot_coordinates)

        coordinates_data: Tuple[np.ndarray, np.ndarray] = (
            np.array(camera_coordinates_list),
            np.array(dobots_coordinates_list),
        )
        
    return coordinates_data

get_sample_points(camera, ctrlDobot)
