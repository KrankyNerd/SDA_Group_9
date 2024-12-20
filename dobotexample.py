"""main function, that controls the loading cycle"""

#1import libraries and classes

import threading

import DoBotArm as dbt
import time

import numpy as np
import cv2
from serial.tools import list_ports

from Camera import Camera

homeX, homeY, homeZ = 170, 0, 30

ctrlDobot = dbt.DoBotArm("COM5", homeX, homeY, homeZ, home= False)

#ctrlDobot.rehome(homeX, homeY, )

myCamera = Camera(address=1)




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

    camera: Camera, dobot: dbt.DoBotArm

) -> tuple[list[np.ndarray], list[np.ndarray]]:

    """

    Obtains a bunch of point samples expressed in both the given cameras' and dobots' frames of reference.

    """


    # README: this implementation currently is based on moving to a couple hardcoded points that *must always* be in the cameras' FOV. There are better options which require more time of implementation, such as having a human move the dobot arm with the keyboard and recording a bunch of points, or a "smart" program that can move the dobot in intervals until it exits the FOV


    # we need a minimum of 4 points to create a homography matrix

    # The more points and the more variation the better

    hardcoded_dobot_poses = [

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

        pose = ctrlDobot.getPosition()  # Call the inherited GetPose method
        dobot_coordinates = pose[0], pose[1], pose[2]  # Extract x, y, z from the returned list
        print(dobot_coordinates)

        camera.run() # process image

        camera_coordinates = camera.get_calibration_marker_as_tuple()
        print(camera_coordinates)

        camera_coordinates_list.append(camera_coordinates)
        dobots_coordinates_list.append(dobot_coordinates)


        coordinates_data: tuple[np.ndarray, np.ndarray] = (

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


sample_points = get_sample_points(myCamera, ctrlDobot)

homography_matrix =  get_homography_matrix(sample_points)

print(homography_matrix)