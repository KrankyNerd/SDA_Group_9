import cv2
import numpy as np

class Camera:
    def __init__(self, resolution=(640, 480), channels=3, address=0, white_balance=True):
        self.resolution = resolution
        self.channels = channels
        self.address = address
        self.white_balance = white_balance
        self.capture = cv2.VideoCapture(self.address, cv2.CAP_DSHOW)  # Use the address for the camera
        self.originalWidth = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.originalHeight = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        if self.capture.isOpened():
            print("Camera opened")
        else:
            print("Error: Could not open camera.")

    def get_image(self):
        ret, frame = self.capture.read()
        if not ret:
            print("Could not capture frame")
            return None
        # Crop the image here (adjust coordinates as needed)
        self.crop_img = frame[157:372, 152:368]  
        return self.crop_img

    def process_image(self, frame):
        grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("grayimg", grayimg)
        _, threshold = cv2.threshold(grayimg, 105, 150, cv2.THRESH_BINARY)
        cv2.imshow("thresholding", threshold)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 200:  # Skip small contours
                continue

            approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
            cv2.drawContours(frame, [contour], 0, (0, 0, 255), 2)
            M = cv2.moments(contour)
            if M['m00'] != 0.0:  # Avoid division by zero
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                
                b, g, r = frame[y, x]

                # Determine shape and label
                if len(approx) == 3:
                    shape_name = 'Triangle'
                elif len(approx) == 4:
                    shape_name = 'Square'
                elif len(approx) == 5:
                    shape_name = 'Pentagon'
                elif len(approx) == 6:
                    shape_name = 'Hexagon'
                else:
                    shape_name = 'Circle'

                # Put text on image
                cv2.putText(frame, shape_name, (x + 2, y - 25),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(b), int(g), int(r)), 2)

        return frame

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()


#this do be just here fore testing purposes #TODO: Delete me
# Create an instance of the Camera class
camera = Camera(address=2)  # Use the correct camera address

# Continuously capture and process images
while True:
    captured_image = camera.get_image()
    
    if captured_image is not None:  # Ensure an image was captured
        processed_image = camera.process_image(captured_image)
        
        # Display the processed image with shapes and labels
        cv2.imshow("Processed Image", processed_image)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
