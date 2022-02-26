# Bodega Billboard

Bodega Billboard is a CircuitPython project built for the Adafruit Matrix Portal. It is an attempt to create a lifecycle for panels that is thrifty with memory and accounts for the most common fetching and drawing routines.

Feel free to do what you want with this project but there is no warranty on anything here as it is a pet project of mine.

## secrets.py

Private configuration is kept in a file at the root of the project named `secrets.py`.

To run this project as is you will need the following values to be set:

```
secrets = {
  'ssid' : 'the name of your wifi network',
  'password' : 'the password of your wifi network',
  'timezone' : 'your tz e.g. America/New_York',
  'openweather_token' : 'token for the openweather api',
  'rapidapi_key': 'api key for the rapid APIs',
  'aio_username': 'adafruit username',
  'aio_key': 'adafruit key'
}
```

Apologies for any non-python patterns in this project. I am a humble admirer of the language but not a part of the community.