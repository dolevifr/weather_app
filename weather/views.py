from django.shortcuts import render
from django.views import View
import requests
from .API_KEY import WEATHER_API_KEY
from .location_api_handler import WeatherAPIWrapper
from datetime import datetime

cities = ["New-York", "Tokyo","Tel Aviv","Dubai"]
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class IndexPageView(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        primary_locations_data = [API_wrapper.get_location_weather_data(city) for city in cities]
        return render(request, 'index_page.html', {"locations_data": primary_locations_data})


class ForcastInfo(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        location = request.GET.get('location')
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=7&aqi=no&alerts=no')
        if response.status_code == 200:
            data = response.json()
            curr_day_num = API_wrapper.get_day_of_week_from_epoch(location)
            return render(request, 'forcast_info.html', {'data': data,'curr_day_num': curr_day_num})
        else: #handles error in page not existing places
            return render(request, 'error_page.html')



