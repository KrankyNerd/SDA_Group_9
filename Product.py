"""
Class Product:

Class for products. 
"""


class Product:
    product_counter = 1  # Class variable to keep track of the ID count
   
    def __init__ (self, ID, product_type, product_colour, pixel_posx, pixel_posy,product_pos):

        self.ID = Product.product_counter  # Assign the current count as ID
        Product.product_counter += 1  # Increment the counter for the next product
        self.product_type = product_type
        self.product_colour = product_colour
        self.pixel_posy = pixel_posy
        self.product_posx = pixel_posx
        self.product_pos = product_pos

    def get_product_ID(self):
        return self.ID

    def get_product_type(self):
        return self.product_type

    def get_product_colour(self):
        return self.product_colour

    def get_pixel_pos(self):
        return self.pixel_pos

    def get_product_pos(self):
        return self.product_pos

    def convert_to_product_pos(pixel_pos): #FIXME:
        placeholder = 0
        return placeholder  
