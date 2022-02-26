import displayio
import gc
from adafruit_fakerequests import Fake_Requests
from billboard.panel import Panel
from billboard.cache import Cache
from secrets import secrets
from config import config

class WeatherPanel(Panel): 
  icons = {
    '01': 0,
    '02': 1,
    '03': 2,
    '04': 3,
    '09': 4,
    '10': 5,
    '11': 6,
    '13': 7,
    '50': 8
  }

  def __init__(self, name, lat, long):
    super(Panel, self).__init__()
    self.name = name
    self.lat = lat
    self.long = long
    self.cache_key = 'weather_' + str(self.lat) + '_' + str(self.long)

  def get_data(self, network):
    gc.collect()
    start_mem = gc.mem_free()
    print( "weather_panel: start get_data : available memory: {} bytes".format(start_mem))
    
    cache = Cache()
    out = cache.get(self.cache_key)
    if out is None:
      if config['environment'] == 'development':
        data = Fake_Requests('/data/weather.json').json()
      else:
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + self.lat + '&lon=' + self.long + '&exclude=minutely,hourly&units=imperial&appid=' + secrets['openweather_token']
        data = network.fetch(url).json() 
      
      out = {
        'current_temp': round(network.json_traverse(data, ['current', 'temp'])),
        'current_weather': self.icons[network.json_traverse(data, ['current', 'weather', 0, 'icon'])[0:2]],
        'todays_high': round(network.json_traverse(data, ['daily', 0, 'temp', 'max'])),
        'todays_low': round(network.json_traverse(data, ['daily', 0, 'temp', 'min'])),
      }
      days = network.json_traverse(data, ['daily'])
      out['days'] = []
      for i in range(len(days)):
        out['days'].append(self.icons[network.json_traverse(days[i], ['weather', 0, 'icon'])[0:2]])
      del data
      gc.collect()
      cache.set(self.cache_key, out, ttl=60*60)
    
    gc.collect()
    end_mem = gc.mem_free()
    print( "weather_panel: end get_data : available memory: {} bytes".format(end_mem) )
    print( "weather_panel: used {} bytes".format(start_mem - end_mem))
    return out
  
  def create(self, matrixportal):
    Panel.create(self, matrixportal)

    data = self.get_data(self.matrixportal.network)

    header = self.get_label(self.name.upper())
    bbx, bby, bbwidth, bbh = header.bounding_box
    header.x = round((self.matrixportal.display.width / 2) - (bbwidth / 2))
    header.y = 3
    self.append(header)

    high_low = self.get_label(str(data['todays_high']) + '\n' + str(data['todays_low']))
    high_low.x = 1
    high_low.y = 12
    self.append(high_low)

    # Current Temperature
    current_temperature = displayio.Group()
    temperature = self.get_label(str(data['current_temp']), font="/fonts/Minecraftia-Regular-8.bdf", scale=2)
    current_temperature.append(temperature)
    degree = self.get_label('°', font="/fonts/Minecraftia-Regular-8.bdf")
    degree.x = temperature.bounding_box[2] * 2
    degree.y = -4
    current_temperature.append(degree)
    current_temperature.x = round((self.matrixportal.display.width / 2) - (temperature.bounding_box[2]))
    current_temperature.y = 21
    self.append(current_temperature)


    # Current Weather Icon
    weather = displayio.OnDiskBitmap('/assets/weather.bmp')
    w_tile_width = 15
    current = displayio.TileGrid(weather, pixel_shader=weather.pixel_shader,
      width = 1,
      height =1,
      tile_width = w_tile_width,
      tile_height = 14
    )
    current[0] = data['current_weather']
    current.x = round(self.matrixportal.display.width - w_tile_width)
    current.y = 9
    self.append(current)

    # Forecast
    tiny_weather = displayio.OnDiskBitmap('/assets/weather-tiny.bmp')
    tw_width = len(data['days'])
    tw_tile_width = 5
    forecast = displayio.TileGrid(tiny_weather, pixel_shader=tiny_weather.pixel_shader,
      width = tw_width,
      height = 1,
      tile_width = tw_tile_width,
      tile_height = 4
    )
    for i in range(len(data['days'])):
      forecast[i] = data['days'][i]
    forecast.x = round((self.matrixportal.display.width - (tw_width * tw_tile_width)) / 2)
    forecast.y = 27
    self.append(forecast)