import board
from digitalio import DigitalInOut, Pull
from adafruit_debouncer import Debouncer


class Buttons:
    def __init__(self, refresh_rate=0.1):
      pin_down = DigitalInOut(board.BUTTON_DOWN)
      pin_down.switch_to_input(pull=Pull.UP)
      self.button_down = Debouncer(pin_down, refresh_rate)
      pin_up = DigitalInOut(board.BUTTON_UP)
      pin_up.switch_to_input(pull=Pull.UP)
      self.button_up = Debouncer(pin_up, refresh_rate)
    
    def update(self):
      self.button_down.update()
      self.button_up.update()
      return self.button_down.fell, self.button_up.fell