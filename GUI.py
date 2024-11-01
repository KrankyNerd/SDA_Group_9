"""
Class GUI:
add_doc_strings_to_classes
This class controls a Graphic User Interface.

"""
import time
from Product import *
from Camera import *
class GUI:
    def __init__(self, resolution, duration, product_list, product_selection):
        self.resolution = resolution
        self.duration = duration
        self.product_list = product_list
        self.product_selection = product_selection #bool to indicate product has been selected

    def start_timer(self, duration):
        """
        Start a timer in miliseconds.
        
        :param duration float: duration of timer.
        :return: true if time has elapsed, false otherwise. 
        """
        start_time=0# when timer starts
        current_time = time.time()
        if current_time - start_time >= duration:
            return True
        else:
            return False      

    def toggle_product_selection(self, product_selection):
        """
        Toggle the state of end-effector responsible for selecting a product.

        :return: None.
        """
        product_selection =not product_selection
        return None
    
    def display_error(self):
        """
        Print a especific error message to terminal.
        
        :return: string. 
        """
    
        return ("Message")

    def instantiate_product(self, product_dict):
        """
        Instantiate a product and append it to the product list. 

        :param product_dict: dictonary containing product data.
        :return: None. 
        """
        product_list=[]
        product = Product(product.ID, product.product_type, product.product_colour, product.pixel_pos, product.product_pos)
        product_list.append(product)
        product_dict ={product.ID:{ 
                       'product_type':product.product_type,
                        'product_colour' :product.product_colour,
                         'pixel_pos': product.pixel_pos,
                          'product_pos': product.product_pos} for product in product_list}

        return None #TODO: add all parameters

    def display_products(self):
        """
        Display all products in product_list on screen.
        """
        frame =camera.get_image()
        cv2.imshow("Product Detection", frame)

        return None
        