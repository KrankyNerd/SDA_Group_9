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

    def instantiate_product(self,detected_shapesdata):#, product_dict):
        """
        Instantiate a product and append it to the product list. 

        :param product_dict: dictonary containing product data.
        :return: None. 
        """
        product_counter =0 # Assign the current count as ID
        
        for product_dict in  detected_shapesdata :
            product = Product(
                ID=product_counter,
                product_type=product_dict["product_type"],
                product_colour=product_dict["product_colour"],
                pixel_posx=product_dict["pixel_posx"],
                pixel_posy=product_dict["pixel_posy"]
            )
            #product = Product(**product_dict)
            self.product_list.append(product)
            product_counter += 1  # Increment the counter for the next product
        

        return self.product_list
    def display_products(self):
        """
        Display all products in product_list on screen.
        """
        for product in self.product_list:
            print(f"Detected Product{product.ID}:{product.product_type}of colour {product.product_colour} at x:{product.pixel_posx} and y{product.pixel_posy}")
        

        return None
    
if __name__ == "__main__": 
    myGUI= GUI(10,500,[],True)
    camera= Camera()
    #we need a loop so that multiple products can be created and appeneded
   
    while True: #not good, infinite loop     
        frame=camera.get_image()
        if frame is not None:
            processed_image, detected_shapesdata = camera.process_image(frame)#detected_shapesdata =camera.process_image(frame)[1]
            print (detected_shapesdata)
            myGUI.instantiate_product(detected_shapesdata)
            myGUI.display_products()
            cv2.imshow("Processed Image", processed_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    
    camera.release()