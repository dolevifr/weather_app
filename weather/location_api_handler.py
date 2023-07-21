import requests
from .API_KEY import WEATHER_API_KEY



class WeatherAPIWrapper:
    def get_location_weather_data(self, location):
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=2&aqi=no&alerts=no')
        if response.status_code == 200:
            return response.json()
        else:
            pass
