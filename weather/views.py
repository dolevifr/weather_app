from django.shortcuts import render
from django.views import View
import requests
from .API_KEY import WEATHER_API_KEY
from .location_api_handler import WeatherAPIWrapper

cities = ["London", "New-York", "Dubai","Tel Aviv"]


class IndexPageView(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        primary_locations_data = [API_wrapper.get_location_weather_data(city) for city in cities]
        return render(request, 'index_page.html', {"locations_data": primary_locations_data})


class ForcastInfo(View):
    def get(self, request):
        location = request.GET.get('location')
        response = requests.get(
            f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=2&aqi=no&alerts=no')
        if response.status_code == 200:
            data = response.json()
        else:
            pass
        return render(request, 'forcast_info.html', {'data': data})
