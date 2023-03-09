from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from billboard.panel_manager import PanelManager
from billboard.weather_panel import WeatherPanel
from billboard.football_panel import FootballPanel
from billboard.date_time_panel import DateTimePanel


class Panels():
  def __init__(self, matrixportal):
    self.matrixportal = matrixportal
    self.display = matrixportal.display
    self.network = matrixportal.network
    
    self.panel_manager = PanelManager()
    self.panel_manager.add_panel(DateTimePanel())
    self.panel_manager.add_panel(FootballPanel())
    # self.panel_manager.add_panel(WeatherPanel('Hoboken', '40.7435', '-74.0291'))
    # self.panel_manager.add_panel(WeatherPanel('Lavalette', '39.9704', '74.0687'))

    font = bitmap_font.load_font("/fonts/Silkscreen-tightest-8.bdf")
    self.loading_label = Label(font, text="LOADING", color=0xFFFFFF)
    self.loading_label.x = self.display.width // 2 - self.loading_label.width // 2
    self.loading_label.y = self.display.height // 2 - self.loading_label.height // 2

    self.display.show(self.loading_label)
    self.panel_manager.get_current_panel().create(self.matrixportal)
    self.display.show(self.panel_manager.get_current_panel())

  def update(self):
    self.panel_manager.get_current_panel().update()

  def next_panel(self):
    self.display.show(self.loading_label)
    self.panel_manager.get_current_panel().destroy()
    self.panel_manager.increment_panel()
    self.panel_manager.get_current_panel().create(self.matrixportal)
    self.display.show(self.panel_manager.get_current_panel())

  def previous_panel(self):
    self.display.show(self.loading_label)
    self.panel_manager.get_current_panel().destroy()
    self.panel_manager.decrement_panel()
    self.panel_manager.get_current_panel().create(self.matrixportal)
    self.display.show(self.panel_manager.get_current_panel())
