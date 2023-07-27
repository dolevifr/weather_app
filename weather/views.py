from django.shortcuts import render
from django.views import View
import requests
from .API_KEY import WEATHER_API_KEY
from .location_api_handler import WeatherAPIWrapper
from .forms import InputForm

cities = ["New-York", "Tokyo", "Rishon-LeZiyyon", "Dubai"]
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class IndexPageView(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        primary_locations_data = [API_wrapper.get_location_weather_data(city).json() for city in cities]

        return render(request, 'index_page.html', {'locations_data': primary_locations_data, 'cities': cities,
                                                   'weather_input_form': InputForm()})



class ForcastInfo(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        location = request.GET.get('location')
        response = API_wrapper.get_location_weather_data(location)
        if response.status_code == 200:
            data = response.json()
            curr_day_num = API_wrapper.get_day_of_week_from_epoch(location)
            return render(request, 'forcast_info.html',
                          {'data': data, 'curr_day_num': curr_day_num, 'days_of_week': days_of_week})
        else:  # handles error in page not existing places
            return render(request, 'error_page.html')



