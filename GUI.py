"""
Class GUI:
This class controls a Graphic User Interface.
"""

import time
from Product import Product
from Camera import Camera
import cv2

class GUI:
    def __init__(self, resolution, duration, product_list, product_selection):
        self.resolution = resolution
        self.duration = duration
        self.product_list = product_list
        self.product_selection = product_selection  # Boolean to indicate if a product has been selected

    def start_timer(self, duration):
        """
        Start a timer in milliseconds.
        
        :param duration: Duration of the timer.
        :return: True if time has elapsed, False otherwise.
        """
        start_time = time.time()
        return (time.time() - start_time) >= duration

    def toggle_product_selection(self):
        """
        Toggle the state of the product selection flag.
        """
        self.product_selection = not self.product_selection

    def display_error(self, message="An error occurred."):
        """
        Print a specific error message to the terminal.
        
        :param message: The error message to display.
        """
        print(f"Error: {message}")

    def instantiate_product(self, detected_shapesdata):
        """
        Instantiate products from detected shapes data and append them to the product list.
        
        :param detected_shapesdata: List of dictionaries containing shape data.
        """
        #Clear productlist at the end of each cycle
        self.product_list =[]
        product_counter = len(self.product_list)  # Continue ID from current list size
        for product_dict in detected_shapesdata:
            product = Product(
                ID=product_counter,
                product_type=product_dict["product_type"],
                product_colour=product_dict["product_colour"],
                pixel_posx=product_dict["pixel_posx"],
                pixel_posy=product_dict["pixel_posy"]
            )
            self.product_list.append(product)
            product_counter += 1

    def display_products(self):
        """
        Display all products in the product list on the screen.
        """
        if not self.product_list:
            print("No products detected.")
            return

        for product in self.product_list:
            print(f"Product {product.ID}: {product.product_type}, Color: {product.product_colour}, "
                  f"Position: ({product.pixel_posx}, {product.pixel_posy})")

if __name__ == "__main__":
    myGUI = GUI(resolution=(640, 480), duration=500, product_list=[], product_selection=True)
    camera = Camera()

    try:
        while True:
            frame = camera.get_image()
            if frame is not None:
                processed_image, detected_shapesdata = camera.process_image(frame)

                # Display the processed image
                cv2.imshow("Processed Image", processed_image)
# Instantiate and display detected products
                myGUI.instantiate_product(detected_shapesdata)
                #myGUI.display_products()
                # Mouse interaction for shape clicks
                def handle_mouse_click(event, x, y, flags, param):
                    if event == cv2.EVENT_LBUTTONDOWN:
                        for shape in detected_shapesdata:
                            if abs(x - shape["pixel_posx"]) < 10 and abs(y - shape["pixel_posy"]) < 10:
                                print(f"Clicked on {shape['product_type']} at ({x}, {y})!")
                                selected_shape=[shape["pixel_posx"],shape["pixel_posy"]]
                                print(selected_shape)

                                break

                cv2.setMouseCallback("Processed Image", handle_mouse_click)
                

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
