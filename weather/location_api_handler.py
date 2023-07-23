import requests
from .API_KEY import WEATHER_API_KEY
from datetime import datetime


class WeatherAPIWrapper:
    def get_location_weather_data(self, location):
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=2&aqi=no&alerts=no')
        if response.status_code == 200:
            return response.json()
        else:
            pass

    def get_hour_minute_from_epoch(self, location):
        response_json= self.get_location_weather_data(location)
        location_data_from_json = response_json['location']
        epoch_timestamp = location_data_from_json['localtime_epoch']
        dt_object = datetime.datetime.fromtimestamp(epoch_timestamp)
        # Format the hours and minutes as a string in "hours:minutes" format
        formatted_time = dt_object.strftime("%H:%M")
        return formatted_time



    def get_day_of_week_from_epoch(self,location):
        response_json = self.get_location_weather_data(location)
        location_data_from_json = response_json['location']
        epoch_timestamp = location_data_from_json['localtime_epoch']
        # Convert epoch time to a datetime object
        dt_object = datetime.fromtimestamp(epoch_timestamp)
        # Get the day of the week (0: Monday, 1: Tuesday, ..., 6: Sunday)
        day_of_week_number = dt_object.weekday()
        return day_of_week_number

