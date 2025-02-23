import cv2
import numpy as np

"""
Class Camera: TEST DOES IT NOT LET ME COMMMIT AHHH

Control a camera object, get images and detect shapes in an image.
"""

class Camera:
    THRESHOLD_VALUE = 102
    MAX_THRESHOLD_VALUE = 150
    MIN_CONTOUR_AREA = 200
    CROP_Y_START, CROP_Y_END, CROP_X_START, CROP_X_END = 169, 394, 213, 432

    def _init_(self, resolution=(640, 480), channels=3, address=0, white_balance=True):
        self.resolution = resolution
        self.channels = channels
        self.address = address
        self.white_balance = white_balance
        self.capture = cv2.VideoCapture(self.address, cv2.CAP_DSHOW)
        self.camera_error = False

        if not self.capture.isOpened():
            self.camera_error = True
            raise Exception("Error: Could not open camera.")
        
        # Set up mouse callback for detecting clicks
        self.contours = []  # Placeholder for contours
        cv2.namedWindow("Processed Image")
        cv2.setMouseCallback("Processed Image", self.handle_mouse_click)

    def get_image(self):
        """the camera captures the image and returns the frame"""
        ret, frame = self.capture.read()
        if not ret:
            print("Could not capture frame")
            return None
        return frame[self.CROP_Y_START:self.CROP_Y_END, self.CROP_X_START:self.CROP_X_END]  

#TODO: add shape_detected bool
    def detect_shape(self, approx):
        """Returns the shape type of a product detected by the camera """
        # Approximate the contour to detect the shape
        if len(approx) == 3:
            return 'Triangle'
        elif len(approx) == 4:
            return 'Square'
        elif len(approx) == 5:
            return 'Pentagon'
        elif len(approx) == 6:
            return 'Hexagon'
        else:
            return 'Circle'

    def process_image(self, frame):
        """Process the image to detect shapes and return contours."""
        #converts captured image to grayscale
        grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("Gray Image", grayimg)

        _, threshold = cv2.threshold(grayimg, self.THRESHOLD_VALUE, self.MAX_THRESHOLD_VALUE, cv2.THRESH_BINARY)
        cv2.imshow("Thresholding", threshold)

        #find the contours in the image
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.contours = contours  # Update the contours for mouse callback
        detected_shapesdata = []  # List to hold detected shape information

        for contour in contours:
            if cv2.contourArea(contour) < self.MIN_CONTOUR_AREA:
                continue

            approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
            cv2.drawContours(frame, [contour], 0, (0, 0, 255), 2)
            
            # Calculate centroid
            M = cv2.moments(contour)# Get the pixel position (center) of the contour

            if M['m00'] != 0.0:  # Avoid division by zero
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                shape_name = self.detect_shape(approx)
                b, g, r = frame[y, x]

                # Put text on image
                cv2.putText(frame, shape_name, (x + 2, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(b), int(g), int(r)), 2)
                # Add pixel coordinates to the image
                cv2.putText(frame, f'({x}, {y})', (x + 2, y + 5),  # Position the coordinates just below the shape
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (int(b), int(g), int(r)), 2)

                # Append detected shape information to the list
                # why? shouldn't this happen in GUI? -isa
                detected_shapesdata.append({
                    'product_type': shape_name,
                    'product_colour': (b, g, r),
                    'pixel_posx': x,
                    'pixel_posy': y      
                })

        return frame, detected_shapesdata  # Return both the processed image and detected shapes

    def handle_mouse_click(self,event, x, y, flags, param):
        """Handle mouse click to check if a point is inside a contour."""
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked_point = (x, y)

            for contour in self.contours:
                result = cv2.pointPolygonTest(contour, clicked_point, False)
                if result >= 0:  # point is inside or on the contour

                    shape_name = self.detect_shape(cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True))  # Detected shape
                    print(f"Clicked on a {shape_name} at {clicked_point}.")
                    break
    def run(self):
        while True:
            captured_image = self.get_image()
            if captured_image is not None:
                processed_image, detected_shapesdata = self.process_image(captured_image)
                cv2.imshow("Processed Image", processed_image)

                # Print detected shapes to the console
                ##for shape_info in detected_shapesdata:
                    #print(f"Detected {shape_info['product_type']} at {shape_info['product_posx']},{shape_info['product_posy']} with color {shape_info['product_color']}")
                   
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()

#TODO: make sure to delete this stuff was just for testing
# Create an instance of the Camera class and run it
#if _name_ == "_main_":