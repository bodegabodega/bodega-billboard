import time
import board
from adafruit_matrixportal.matrixportal import MatrixPortal
from billboard.buttons import Buttons
from billboard.panels import Panels
from billboard.time_keeper import TimeKeeper
from billboard.auto_advance import AutoAdvance

REFRESH_RATE = 0.01

# --- Secrets setup ---
# try:
#     from secrets import secrets
# except ImportError:
#     print("WiFi secrets are kept in secrets.py, please add them there!")
#     raise

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

# --- Buttons setup ---
buttons = Buttons(REFRESH_RATE)

# --- Timekeeper setup ---
timekeeper = TimeKeeper()

# --- Panels setup ---
panels = Panels(matrixportal)

# --- AutoAdvance setup ---
auto_advance = AutoAdvance(panels.next_panel)

# --- Run Loop ---
while True:
  down, up = buttons.update()
  if down:
    auto_advance.increment_interval()
  if up:
    panels.next_panel()
  timekeeper.update()
  panels.update()
  time.sleep(REFRESH_RATE)