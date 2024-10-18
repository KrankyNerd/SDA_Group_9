#here the possible shapes to be picked are shown
#and the user can select one for the entire process.
#You could let the UI randomly (color and shape) select which shapes (at least three) must be placed on the loading area 
from Product import *
class GUI:
    def __init__(self, resolution, duration,product, product_list, product_selection):
        self.resolution = resolution
        self.duration = duration
        self.product_list = product_list
        self.product_selection = product_selection

    def start_timer():
        return None

    def time_elapsed():
        placeholder = 0
        return placeholder #TODO:

    
    def display_error():
        return ("Message") #TODO:

    def instantiate_product(self):
        self.product=Product(ID, product_type, product_colour, pixel_pos, product_pos)
        return None

    def display_products():
        return None
    def toggle_product_selection(product_selection):
        return None  