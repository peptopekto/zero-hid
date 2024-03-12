import time
from . import defaults
from .hid.mouse import relative_mouse_event, absolute_mouse_event
from typing import SupportsInt

class RelativeMoveRangeError(Exception):
    pass

class Mouse:
    def __init__(self, dev = None, absolute = False) -> None:
        self.__setup_device(dev, absolute)
        self.__setup_move(absolute)
        self.__send_mouse_event = absolute_mouse_event if absolute else relative_mouse_event # dynamic mouse event method
        self.buttons_state = 0x0
        
    def __setup_device(self, dev, absolute: bool):
        if dev is None:
            dev = defaults.ABSOLUTE_MOUSE_PATH if absolute else defaults.RELATIVE_MOUSE_PATH
        if not hasattr(dev, 'write'): # check if file like object
            self.dev = open(dev, 'ab+')
        else:
            self.dev = dev
    
    def __setup_move(self, absolute: bool):
        self.move = self.__move_absolute if absolute else self.__move_relative # dynamic move method

    def left_press(self):
        self.buttons_state |= 0x1  # set left button bit
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def left_release(self):
        self.buttons_state &= ~0x1  # clear left button bit
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def right_press(self):
        self.buttons_state |= 0x2  # set right button bit
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def right_release(self):
        self.buttons_state &= ~0x2  # clear right button bit
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def middle_press(self):
        self.buttons_state |= 0x4  # set middle button bit
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def middle_release(self):
        self.buttons_state &= ~0x4  # clear middle button bit
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def clickLeftButton(self, delay: int = 0.025):
        self.left_press()
        time.sleep(delay)
        self.left_release() 
    
    def clickRightButton(self, delay: int = 0.025):
        self.right_press()
        time.sleep(delay)
        self.right_release()
    
    def clickMiddleButton(self, delay: int = 0.025):
        self.middle_press()
        time.sleep(delay)
        self.middle_release()

    def pressAnyButton(self, button: int):
        if not 1 <= button <= 7:
            raise ValueError("Button should be in range of 1 to 7")
        self.buttons_state |= button
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def releaseAnyButton(self, button: int):
        if not 1 <= button <= 7:
            raise ValueError("Button should be in range of 1 to 7")
        self.buttons_state &= ~button
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, 0)

    def clickAnyButton(self, button: int, delay: int = 0.025):
        self.pressAnyButton(button)
        time.sleep(delay)
        self.releaseAnyButton(button)

    def scroll_y(self, position: int):
        """
        scroll in y axis (vertical)
        y should be in range of -127 to 127
        """
        if not -127 <= position <= 127: 
            raise RelativeMoveRangeError(f"Value of y {position} out of range (-127 - 127)")
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, position, 0)

    def scroll_x(self, position: int):
        """
        scroll in x axis (horizontal)
        x should be in range of -127 to 127
        """
        if not -127 <= position <= 127: 
            raise RelativeMoveRangeError(f"Value of x: {position} out of range (-127 - 127)")
        self.__send_mouse_event(self.dev, self.buttons_state, 0, 0, 0, position)

    def raw(self, buttons_state, x, y, scroll_y, scroll_x):
        """
        Control the way you like
        """
        self.__send_mouse_event(self.dev, self.buttons_state, x, y, scroll_y, scroll_x)

    def __move_relative(self, x, y):
        """
        move the mouse in relative mode
        x,y should be in range of -127 to 127
        """
        if not -127 <= x <= 127: 
            raise RelativeMoveRangeError(f"Value of x: {x} out of range (-127 - 127)")
        if not -127 <= y <= 127:
            RelativeMoveRangeError(f"Value of y: {y} out of range (-127 - 127)")
        self.__send_mouse_event(self.dev, self.buttons_state, x, y, 0, 0)
        
    def __move_absolute(self, x, y):
        if not 0 <= x <= 65535: 
            raise RelativeMoveRangeError(f"Value of x: {x} out of range (0 - 65535)")
        if not 0 <= y <= 65535:
            RelativeMoveRangeError(f"Value of y: {y} out of range (0 - 65535)")
        self.__send_mouse_event(self.dev, self.buttons_state, x, y, 0, 0)
        
    def __enter__(self):
        return self

    def _clean_resources(self):
        self.dev.close()    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clean_resources()
        
    def close(self):
        self._clean_resources()