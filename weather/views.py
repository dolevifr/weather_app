from django.shortcuts import render
from django.views import View
import requests
from .API_KEY import WEATHER_API_KEY
from .location_api_handler import WeatherAPIWrapper
from .forms import InputForm_must, InputForm_not_must

cities = ["New-York", "Tokyo", "Rishon-LeZiyyon", "Dubai"]
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class IndexPageView(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        primary_locations_data = [API_wrapper.get_location_weather_data(city).json() for city in cities]
        return render(request, 'index_page.html', {'locations_data': primary_locations_data, 'cities': cities,
                                                   'weather_input_form_must': InputForm_must(),
                                                   'weather_input_form_not_must': InputForm_not_must()})


class ForcastInfo(View):
    def get(self, request):
        API_wrapper = WeatherAPIWrapper()
        #location = request.GET.get('location')
        location, start_date, end_date= API_wrapper.extract_data_must(request)
        response = API_wrapper.get_location_weather_data(location)
        location_not_must, start_date_not_must, end_date_not_must = API_wrapper.extract_data_not_must(request)
        if response.status_code == 200:
            data = response.json()
            curr_day_num = API_wrapper.get_day_of_week_from_epoch(location)
            return render(request, 'forcast_info.html',
                          {'data': data, 'curr_day_num': curr_day_num, 'days_of_week': days_of_week,
                           'location': location, 'end_date': end_date,
                           'start_date_must': start_date, 'location_not_must': location_not_must,
                           'end_date_not_must': end_date_not_must, 'start_date_not_must': start_date_not_must})
        else:  # handles error in page not existing places
            return render(request, 'error_page.html')
