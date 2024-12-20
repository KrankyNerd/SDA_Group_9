"""main function, that controls the loading cycle"""

# 1import libraries and classes
import threading
import DoBotArm as dbt
import time
import Conveyor
import Camera
import GUI
import Dobot
import numpy as np
import cv2
import EndEffector
from typing import List, Tuple

# from serial.tools import list_ports


# 2 define constants
homeX, homeY, homeZ = 170, 0, 0


# 3 Create objects of the needed classes
conveyor = Conveyor(True, 0)
camera = Camera(address=2)
end_effector = EndEffector(False)
myGUI = GUI(
    0, 5000, [], False
)  # resolution, timer duration, product list, product selection
myDobot = dbt.DoBotArm(
    "COM3", homeX, homeY, homeZ, home=False
)  # FIX THIS, should be from Dobot.py

print("starting")

myDobot.moveHome()  # this needs to be here for some reason
myDobot.moveArmXYZ(x=170, y=50, z=0)
myDobot.moveArmXYZ(x=170, y=0, z=0)
time.sleep(2)
# 4 Camera setup and  Camera image detection
camera.run()

# 5a GUI display
myGUI.display_products()
# 5b User input handling
# 6 Moving product

# 6a obtain product position and move to it

# 6b pick product :lower arm, toggle end effector, raise arm
myDobot.moveArmRelXYZ(0, 0, 40)
myDobot.moveArmXYZ(x=170, y=0, z=-7)
myDobot.toggleSuction()
time.sleep(5)
# 6 c move to conveyor position, lower arm, toggle end effector, raise arm
myDobot.moveArmRelXYZ(0, 0, 40)
time.sleep(5)
myDobot.toggleSuction()

# 6d home dobot, move conveyor, stop conveyor
##conveyor.move_conveyor(True, 15000)#start conveyor
time.sleep(5)  # delay
# conveyor.move_conveyor(True, 0)#stops conveyor
camera.release()

# ctrlDobot.SetConveyor(True, 15000)#start conveyor
# time.sleep(5)#delay
# ctrlDobot.SetConveyor(True, 0)#stops conveyor
# #def SetConveyor(self, enabled, speed = 15000):


def get_sample_points(
    camera: Camera, dobot: Dobot
) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Obtains a bunch of point samples expressed in both the given cameras' and dobots' frames of reference.
    """

    # README: this implementation currently is based on moving to a couple hardcoded points that *must always* be in the cameras' FOV. There are better options which require more time of implementation, such as having a human move the dobot arm with the keyboard and recording a bunch of points, or a "smart" program that can move the dobot in intervals until it exits the FOV

    # we need a minimum of 4 points to create a homography matrix
    # The more points and the more variation the better
    hardcoded_dobot_poses = [
        (170, 0, 0),
        (220, -60, 0),
        (0, 0, 0),
        (0, 0, 0),
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



def get_homography_matrix(sample_points) -> np.ndarray:  # to call once in init
    """
    Returns a transformation matrix from camera coordinates to arm coordinates. This can be used to then transform between frames of reference.

    Returns:
        np.ndarray: homography matrix
    """

    camera_points = sample_points[0]
    dobot_points = sample_points[1]

    # tests
    assert len(camera_points) == len(
        dobot_points
    ), "different amount of camera and dobot point samples"
    assert (
        len(camera_points) >= 4
    ), f"Too little sample points ({len(camera_points)} to calculate a homography matrix, 4 or more are needed)"
    assert len(camera_points) == len(
        {tuple(pt) for pt in camera_points}
    ), "Camera points are not unique"
    assert len(dobot_points) == len(
        {tuple(pt) for pt in dobot_points}
    ), "Dobot points are not unique"

    # add artificial 3rd coordinates for the math to math
    camera_points = [
        np.array([point[0], point[1], 1.0]).reshape(3, 1) for point in camera_points
    ]
    dobot_points = [
        np.array([point[0], point[1], 1.0]).reshape(3, 1) for point in dobot_points
    ]

    # compute the matrix
    homography_matrix, _ = cv2.findHomography(camera_points, dobot_points)

    return homography_matrix


def convert_camera2dobot_coordinates(
    homography_matrix, camera_point
) -> Tuple[int, int]:

    assert (
        len(camera_point) == 2
    ), f"Expected 2 values for the camera point, got {len(camera_point)} instead"

    # add artificially z coordinate for matrix multiplication to work
    camera_point = np.array([camera_point[0], camera_point[1], 1.0])
    # maybe you need to reshape to a column vector, instead of a row vector
    # camera_point = camera_point.reshape(3,1)
    dobot_point = np.dot(homography_matrix, camera_point)
    dobot_point /= dobot_point[2]  # Normalize, not sure why

    return dobot_point


"""
Plan for today

1. [ ] Get white square (dobot) coordinates
2. [ ] Implement the rest of get_sample_points()
    2.1 [x] manage to move the dobot
    2.2 [x] manage to get the dobot current coordinates
3. [x] Find good hardcoded_points for the dobot to collect samples
4. [ ] Run get_sample_points() and make sure the output makes sense, it a pair (tuple) of lists of points, the first from the camera and the second from the dobot
5. [ ] Pass the collected points to get_homography_matrix() and verify it returns a 3x3 numpy matrix with floating values inside
6. [ ] Now try using all this to make the robot go to a desired point in the camera, if it is simpler then just try making it go to a shape (instead of creating another way of selecting a point)
"""
