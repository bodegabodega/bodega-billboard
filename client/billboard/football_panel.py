import gc
import displayio
import adafruit_imageload
from adafruit_fakerequests import Fake_Requests
from billboard.panel import Panel
from billboard.cache import Cache
from secrets import secrets
from config import config

class FootballPanel(Panel):
  results = {
    'W': 0,
    'L': 1,
    'D': 2
  }

  def __init__(self, league = 39, team = 42, season = 2021):
    super(Panel, self).__init__()
    self.league = league
    self.team = team
    self.season = season
    self.cache_key = 'football_panel_' + str(league) + '_' + str(team) + '_' + str(season)
  
  def get_data(self, network):
    cache = Cache()
    out = cache.get(self.cache_key)

    if out is None:
      if config['environment'] == 'development':
        data = Fake_Requests('/data/arsenal.json').json() 
      else:
        # url = 'https://nupwhs7rhuplxmblga2s6k4t3y0wpepy.lambda-url.us-east-1.on.aws?season=' + str(self.season) + '&team=' + str(self.team) + '&league=' + str(self.league)
        # print(url)
        headers = {"x-rapidapi-key": secrets['rapidapi_key']}
        data = network.fetch('https://v3.football.api-sports.io/teams/statistics?season=' + str(self.season) + '&team=' + str(self.team) + '&league=' + str(self.league), headers=headers).json()
     
        # data = network.fetch(url).json()
      out = {
        'team': network.json_traverse(data, ['name']),
        'form': network.json_traverse(data, ['form']),
        'wins': network.json_traverse(data, ['totalWins']),
        'losses': network.json_traverse(data, ['totalLoses']),
        'draws': network.json_traverse(data, ['totalDraws']),
        'goals_for': network.json_traverse(data, ['totalGoalsFor']),
        'goals_against': network.json_traverse(data, ['totalGoalsAgainst']),
      }
      del data
      gc.collect()
      cache.set(self.cache_key, out, ttl=60*60*24)
    return out
  
  def create(self, matrixportal):
    data = self.get_data(matrixportal.network)
    
    header = self.get_label(data['team'].upper())#, color=0xEF0107)
    header.y = 3
    header.x = 1
    self.append(header)

    form = list(data['form'][-30:])
    sprite_sheet, palette = adafruit_imageload.load('/assets/wld.bmp',
      bitmap=displayio.Bitmap,
      palette=displayio.Palette
    )
    palette.make_transparent(3)
    wld = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
      width = len(form),
      height = 1,
      tile_width = 2,
      tile_height = 1
    )
    for i in range(len(form)):
      wld[i] = self.results[form[i]]
    wld.x = 1
    wld.y = 7
    self.append(wld)

    points = (data['wins'] * 3) + data['draws']
    goal_difference = data['goals_for'] - data['goals_against']
    record = "{}W {}L {}D\n{} POINTS\n{} GA".format(data['wins'], data['losses'], data['draws'], points, goal_difference)

    record = self.get_label(record)#, font="/fonts/Minecraftia-Regular-8.bdf")
    record.y = 11
    record.x = 1
    self.append(record)