import time
import math
from billboard.panel import Panel
from config import config
from billboard.time_keeper import TimeKeeper

class DateTimePanel(Panel):
  colors = [
    0x001070, # 1-4
    0xFFA080, # 5-8
    0xFFD050, # 9-12
    0xB0C0E0, # 13-16
    0x306070, # 17-20
    0x204080 # 21-24
  ]
  def __init__(self):
    super(Panel, self).__init__()
  
  def get_data(self):
    if not self.synchronized:
      self.matrixportal.network.get_local_time()
      self.synchronized = True
    return time.localtime()
  
  def update_display(self):
    (year, month, day, hours, minutes, sec, wday, yday, isdst) = self.get_data()  # Get the time values we need
    color = self.colors[math.floor((hours / 24) * len(self.colors))]
    self.time_label.color =  color
    ampm = "AM"
    if hours > 12:  # Handle times later than 12:59
        hours -= 12
        ampm = "PM"
    elif not hours:  # Handle times between 0:00 and 0:59
        hours = 12
    self.time_label.text = "{hours}:{minutes:02d}{ampm}".format(
        hours=hours, minutes=minutes, ampm=ampm
    )
    self.date_label.text = "{month}/{day}/{year}".format(
        month=month, day=day, year=year
    )
    if self.time_string_length != len(self.time_label.text):
      print("updating time string length") 
      self.time_string_length = len(self.time_label.text)
      self.time_label.x = self.matrixportal.display.width // 2 - self.time_label.width // 2
      self.time_label.y = self.matrixportal.display.height // 2 - self.time_label.height
    if self.date_string_length != len(self.date_label.text):
      print("Updating date layout")
      self.date_string_length = len(self.date_label.text)
      self.date_label.x = self.matrixportal.display.width // 2 - self.date_label.width // 2
      self.date_label.y = self.matrixportal.display.height // 2 #self.date_label.height
  
  def update(self):
    self.update_display()

  def synchronize(self):
    print("Synchronizing time")
    self.synchronized = False
  
  def create(self, matrixportal):
    self.matrixportal = matrixportal

    self.time_string_length = None
    self.date_string_length = None
    self.synchronized = (config['environment'] == 'development')

    self.time_label = self.get_label()
    self.append(self.time_label)
    self.date_label = self.get_label()
    self.append(self.date_label)

    self.update_display()

    TimeKeeper().add_listener('datetimepanel', self.synchronize)

  def destroy(self):
      super().destroy()
      del self.time_string_length
      del self.date_string_length
      del self.synchronized
      TimeKeeper().remove_listener('datetimepanel')