from Camera import *


class Dobot:
    def __init__(
        self,
        current_pos,
        current_x,
        current_y,
        current_z,
        desired_pos,
        desired_x,
        desired_y,
        desired_z,
        home_pos,
        error,
        moving_x,
        moving_y,
        moving_z,
        end_pos,
        dobot_serial_timeout,
    ):
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

    def go_to_pos():  # no Z movement

        # x = circle1.pixel_pos.x * ratio
        # y = circle1.pixel_pos.y * ratio

        # Dobot.movearm(x, y, z)

        return None

    def get_current_pos():
        pass

    def get_desired_pos():
        placeholder = 0
        return placeholder  # TODO:

    def pick():  # platform + object z
        ctrlDobot.toggleSuction()
        # Dobot.moveArm(x,y,(home(50) to top of object(21.5)))
        return None

    def place():  # conveyor z
        # Dobot.moveArm(x,y,(Conveyor Height(45.5)+object Height(21.5)))
        ctrlDobot.toggleSuction()
        return None

    def get_ratio():  # to call once in init
        ctrlDobot.moveHome()

        # getting first value
        Camera.run()
        pixel_pos_1 = get_pixel_pos(detected_shapesdata)
        # getting second value
        ctrlDobot.moveArmXYZ(220, -60, 0)
        pixel_pos_2 = get_pixel_pos(detected_shapesdata)


        # get-posX and Y of white cube
        # once detected get pixel_pos
        # move arm x,y by n-amount, get-pos
        # get pixel pos
        # ratio = pixel_pos-pixelpos0/ get_pos - get_pos0
        return ratio

    def get_pixel_pos(detected_shapesdata):
        """
        Extracts the 'product_posx' and 'product_posy' from the first element of the detected shapes list.

        Args:
            detected_shapes (list): A list of dictionaries containing shape data.

        Returns:
            tuple: A tuple containing (product_posx, product_posy) of the first detected shape,
                or None if the list is empty.
        """

        if detected_shapesdata:
            first_shape = detected_shapesdata[0]
            return first_shape["product_posx"], first_shape["product_posy"]
        else:
            return None
