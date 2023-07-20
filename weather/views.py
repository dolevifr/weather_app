from django.shortcuts import render
from django.views import View
import requests
from django.http import HttpResponse
from .API_KEY import WEATHER_API_KEY

class IndexPageView(View):
    def get(self, request):
        return render(request, 'index_page.html')


class ForcastInfo(View):
    def get(self,request):
        location = request.GET.get('location')
        response = requests.get(f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=2&aqi=no&alerts=no')
        if response.status_code == 200:
            data = response.json()
            # Process the data
        else:
            pass
        return render(request, 'forcast_info.html', {'data': data})