"""
Class GUI:
add_doc_strings_to_classes
This class controls a Graphic User Interface.

"""

class GUI:
    def __init__(self, resolution, duration, product_list, product_selection):
        self.resolution = resolution
        self.duration = duration
        self.product_list = product_list
        self.product_selection = product_selection

    def start_timer(self, duration):
        """
        Start a timer in miliseconds.
        
        :param duration float: duration of timer.
        :return: true if time has elapsed, false otherwise. 
        """
        return None
      

    def toggle_product_selection(self, product_selection):
        """
        Toggle the state of end-effector responsible for selecting a product.

        :return: None.
        """
        return None
    
    def display_error(self):
        """
        Print a especific error message to terminal.
        
        :return: string. 
        """
    
        if dobot.dobot_serial_timeout
            return ("ERROR: no Dobot communication.")

        # add if statements for all possible errors

        return ("Message")

    def instantiate_product(self, product_dict):
        """
        Instantiate a product and append it to the product list. 

        :param product_dict: dictonary containing product data.
        :return: None. 
        """
    
        return None #TODO: add all parameters

    def display_products(self):
        """
        Display all products in product_list on screen.
        """
        return None
        