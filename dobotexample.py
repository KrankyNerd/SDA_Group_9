"""testing moving the arm and changing coordinates"""

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

print("homing finished")

time.sleep(1)

#ctrlDobot.moveArmXYZ(175, -25, 20)

#ctrlDobot.moveArmXYZ(145, -20, 20)

#ctrlDobot.moveArmXYZ(160, 10, 20)

#ctrlDobot.moveArmXYZ(150, 0, 20)

#ctrlDobot.moveArmXYZ(20, -220, 30) #correct coordinates for conveyor


#ctrlDobot.DisconnectDobot()

# def SetConveyor(self, enabled, speed = 15000):

# ------------------------- methods ------------------------------

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

def get_homography_matrix(sample_points) -> np.ndarray:
    """
    Returns a transformation matrix from camera coordinates to arm coordinates.
    """

    camera_points = np.array(sample_points[0])  # Convert to NumPy array
    dobot_points = np.array(sample_points[1])   # Convert to NumPy array

    # Ensure points have the correct shape (N, 2)
    #assert camera_points.shape[1] == 2, "Camera points must be of shape (N, 2)"
    #assert dobot_points.shape[1] == 2, "Dobot points must be of shape (N, 2)"

    # compute the matrix
    homography_matrix, _ = cv2.findHomography(camera_points, dobot_points)

    return homography_matrix

def convert_camera2dobot_coordinates(
    homography_matrix, camera_point
) -> tuple[int, int]:

  #  assert (
   #     len(camera_point) == 2
  #  ), f"Expected 2 values for the camera point, got {len(camera_point)} instead"

    # add artificially z coordinate for matrix multiplication to work
    camera_point = np.array([camera_point[0], camera_point[1], 1.0])
    # maybe you need to reshape to a column vector, instead of a row vector
    # camera_point = camera_point.reshape(3,1)
    dobot_point = np.dot(homography_matrix, camera_point)
    dobot_point /= dobot_point[2]  # Normalize, not sure why

    return dobot_point


#------------------------ end of methods -------------------------



sample_points = get_sample_points(myCamera, ctrlDobot)

homography_matrix =  get_homography_matrix(sample_points)

# arm get out of camera pov
print("arm go away")
ctrlDobot.moveArmXYZ(None, -200, 30)
time.sleep(2)
ctrlDobot.moveArmXYZ(80, -200, 30)
time.sleep(2)

#run camera
print("camera go flash")
myCamera.run()
time.sleep(2)

detected_shapesdata = myCamera.run()  # Run and retrieve detected shapes data

# Process detected shapes
if detected_shapesdata:
    for shape in detected_shapesdata:

        positions = [(shape['pixel_posx'], shape['pixel_posy']) for shape in detected_shapesdata]
else:
    print("No shapes detected.")

square_coordinates = positions[0]

converted_coordinates = convert_camera2dobot_coordinates(homography_matrix, square_coordinates)

print("arm go square")


ctrlDobot.moveArmXYZ(160, -200, 30)
ctrlDobot.moveHome()

ctrlDobot.moveArmXYZ(square_coordinates[0], None, 30)

time.sleep(2)
print("Yes")
ctrlDobot.moveArmXYZ(square_coordinates[0], square_coordinates[1], 30)

ctrlDobot.DisconnectDobot()