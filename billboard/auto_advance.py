from billboard.time_keeper import TimeKeeper

INIT_INTERVAL = 10
INTERVAL_INCREMENT = 10
MAX_INTERVAL = 600
LISTENER_NAME = 'auto_advance'

class AutoAdvance:
  def __init__(self, advance_fn):
    self.advance_fn = advance_fn
    self.advance_interval = INIT_INTERVAL
    self.refresh_listener()
  
  def increment_interval(self):
    self.advance_interval += INTERVAL_INCREMENT
    if(self.advance_interval > MAX_INTERVAL):
      self.advance_interval = 0
    self.refresh_listener()

  def refresh_listener(self):
    TimeKeeper().remove_listener(LISTENER_NAME)
    if self.advance_interval != 0:
      TimeKeeper().add_listener(LISTENER_NAME, self.advance_fn, self.advance_interval)