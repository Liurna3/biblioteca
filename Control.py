import pygame
import math

class Control:
    """Aqui se guardan los controles del juego"""

    # tipos de controles
    UNDEFINED = -1
    JOYSTICK = 0
    KEYBOARD = 1

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    FIRE = 4
    
    def __init__(self,
                 control_id = -1,
                 key_left = None,
                 
                 key_right = None,
                 key_up = None,
                 key_down = None,
                 key_fire = None):
        
        self.device_type = Control.UNDEFINED
        self.device_id = control_id

        self._left = key_left
        self._right = key_right
        self._up = key_up
        self._down = key_down
        self._fire = key_fire

        self.buttons = {
            Control.LEFT: 0,
            Control.RIGHT: 0,
            Control.UP: 0,
            Control.DOWN: 0,
        }
        
        if Control.valid_joystic_device_number(control_id):
            self.device_type = Control.JOYSTICK
            self._joystick = Control.setup_joystick(control_id)
            
        else:
            self.device_type = Control.KEYBOARD
        

    def get(self,button):
        self.update()
        return self.buttons[button]
        
    def update(self):
        """Actualiza el estado de los botones"""
        if self.device_type == Control.JOYSTICK:
            radio_raw = self._joystick.get_axis(0)
            radio = math.floor(radio_raw / 0.5) * 0.5 + 0.5
            
            self.buttons[Control.LEFT] = radio < 0
            self.buttons[Control.RIGHT] = radio > 0
            self.buttons[Control.UP] = self._joystick.get_button(0)
            self.buttons[Control.FIRE] = self._joystick.get_button(0)
            return
            

        if self.device_type == Control.KEYBOARD:
            key = pygame.key.get_pressed()
            self.buttons[Control.LEFT] = key[self._left]
            self.buttons[Control.RIGHT] = key[self._right]
            self.buttons[Control.UP] = key[self._up]
            self.buttons[Control.DOWN] = key[self._down]
            self.buttons[Control.FIRE] = key[self._fire]
            return
            
    @classmethod
    def setup_joystick(self, control_id):
        return pygame.joystick.Joystick(control_id)
        
    @classmethod
    def valid_joystic_device_number(cls, control_id):
        if control_id < 0:     # el id minimo de controles es 0
            return False
        
        if  control_id > pygame.joystick.get_count()-1:
            return False

        print(pygame.joystick.get_count())
        return True

    
