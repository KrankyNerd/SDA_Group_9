"""Class End Effector:

Control a boolean suction end-effector. 
"""

class EndEffector:
    def __init__(self, state: bool = False):
        """Initialize a suction end-effector object.
    
        :param: 
        state of the suction end-effector.
        """
        self.state = state

    def toggle_state(self) -> None:
        self.state = not self.state   
        return None
    
    def get_state(self) -> bool:
        return self.state
    