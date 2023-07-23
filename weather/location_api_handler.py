import requests
from .API_KEY import WEATHER_API_KEY
from datetime import datetime

#this wrapper helps me handle the api
class WeatherAPIWrapper:
    def get_location_weather_data(self, location):
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=7&aqi=no&alerts=no')
        return response

    def get_day_of_week_from_epoch(self,location):
        response_json = self.get_location_weather_data(location).json()
        location_data_from_json = response_json['location']
        epoch_timestamp = location_data_from_json['localtime_epoch']
        # Convert epoch time to a datetime object
        dt_object = datetime.fromtimestamp(epoch_timestamp)
        # Get the day of the week, 0 is monday 6 is sunday
        day_of_week_number = dt_object.weekday()
        return day_of_week_number

