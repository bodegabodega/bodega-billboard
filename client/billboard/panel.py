import displayio
import gc
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.bitmap_label import Label

class Panel(displayio.Group):
    def __init__(self):
        pass

    def create(self, matrixportal):
        self.matrixportal = matrixportal
  
    def destroy(self):
        while len(self) > 0:
            item = self.pop()
            del item
        gc.collect()
    
    def update(self):
        pass

    def get_label(self, text = "", font="/fonts/Silkscreen-tightest-8.bdf", color=0xFFFFFF, scale=1):
        font = bitmap_font.load_font(font)
        label = Label(font, text=text, color=color, scale=scale, line_spacing=.9)
        return label