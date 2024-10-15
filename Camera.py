import cv2

class Camera:
    def __init__(self, resolution, channels, address, white_balance, camera_error, image_path, product_detected, product_list,product_dict, product_colour):
        self.resolution = resolution
        self.channels = channels
        self.address = address
        self.white_balance = white_balance
        self.camera_error = camera_error
        self.image_path = image_path
        self.product_detected = product_detected
        self.product_list = product_list
        self.product_dict = product_dict
        self.product_colour = product_colour
        
        #init camera
        self.capture = cv2.VideoCapture(2, cv2.CAP_DSHOW) # 2 being the external camera on levin's Laptop
        self.originalWidth = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.originalHeight = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_image(self):
        
        return None

    def process_image(self.image_path): #TODO:
        return None

    