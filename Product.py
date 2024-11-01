"""
Class Product:

Class for products. 
"""


class Product:

    def __init__ (self, ID, product_type, product_colour, pixel_pos):
        self.__ID = ID                     
        self.__product_type = product_type  
        self.__product_colour = product_colour  
        self.__pixel_pos = pixel_pos       

    # getter methods
    def get_product_ID(self):
        return self.__ID

    def get_product_type(self):
        return self.__product_type

    def get_product_colour(self):
        return self.__product_colour

    def get_pixel_pos(self):
        return self.__pixel_pos
