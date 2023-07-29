import requests
from .API_KEY import WEATHER_API_KEY
from datetime import datetime
from .forms import InputForm_must, InputForm_not_must

#this wrapper helps handle the api
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

    def extract_data_not_must(self, request):
        form = InputForm_not_must(request.GET)
        if form.is_valid():
            # Extract the data from the form fields
            location_not_must = form.cleaned_data['location_not_must']
            start_date_not_must = form.cleaned_data['start_date_not_must']
            end_date_not_must = form.cleaned_data['end_date_not_must']
            return location_not_must, start_date_not_must, end_date_not_must
        else:
            return None,None,None

    def extract_data_must(self, request):
        form = InputForm_must(request.GET)
        if form.is_valid():
            # Extract the data from the form fields
            location = form.cleaned_data['location']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            return location, start_date, end_date

        else:
            return None,None,None





    def what_to_wear_from_data(self,location,start_date,end_date,must):
        if must == True:
            date_difference = end_date - start_date
            days_different = date_difference.days
            response = self.get_location_weather_data(location)




