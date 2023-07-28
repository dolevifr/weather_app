from django import template
from datetime import datetime
from django.utils.safestring import mark_safe
register = template.Library()
from weather.location_api_handler import WeatherAPIWrapper

#the template tags enable me to write functions here and implement them quite simply in the html files

#starts with monday because default python functions supports weeks starting with monday
days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#dict of pathes to images of what to wear
picture_paths_dict = {'hot_with_hat': "images/summer_cap.png" , 'hot_without_hat': "images/summer.png",
                      'cold_with_hat': "images/fall_cap.png",'cold_without_hat': "images/fall.png",
                      'freezing': "images/winter.png"}

#return day of the week number according to list above from epoch
@register.filter("epoch_to_day")
def epoch_to_day(epoch_timestamp):
    dt_object = datetime.fromtimestamp(epoch_timestamp)
    day_of_week_number = dt_object.weekday()
    return days_of_week[day_of_week_number]

#simple clothes choosing app
@register.filter("clothes_to_wear")
def clothes_to_wear(weather_json_data):
    wear_hat = False
    current = weather_json_data["current"]
    curr_temp = current["temp_c"]
    curr_UV = current["uv"]
    wind_speed_kph = current["wind_kph"]
    if curr_UV > 4:
        wear_hat = True
    if curr_temp >= 25:
            return picture_paths_dict["hot_with_hat"] if wear_hat else picture_paths_dict["hot_without_hat"]
    if 20 <= curr_temp < 25 and wind_speed_kph <= 15:
        return picture_paths_dict["hot_with_hat"] if wear_hat else picture_paths_dict["hot_without_hat"]
        #short clothes
    elif 20 <= curr_temp < 25 and wind_speed_kph > 15:
        return picture_paths_dict["cold_with_hat"] if wear_hat else picture_paths_dict["cold_without_hat"]
        #long clothes
    elif 15 < curr_temp < 20:
        return picture_paths_dict["cold_without_hat"]
    else:
        #below 15C degrees
        return picture_paths_dict["freezing"]

#i thought it could be nice to add icons based on daily weather, only supports two icons because the api is poor about daily clouds
@register.filter("weather_icon")
def weather_icon(day_data):
    single_day = day_data["day"] #API doesnt provide daily cloud percentage, for next time need to choose a better API
    chance_of_rain = single_day["daily_chance_of_rain"]
    if chance_of_rain > 20:
        return "fa-solid fa-cloud-rain"
    else:
        return "fa-solid fa-cloud-sun"


@register.filter("clothes_to_wear_in_words")
def clothes_to_wear_in_words(weather_json_data_daily):#forecast.forecastday[index]
    wear_hat = False
    day = weather_json_data_daily["day"]
    avg_temp = day["avgtemp_c"]
    curr_UV = day["uv"]
    if curr_UV > 4:
        wear_hat = True
    if avg_temp >= 22:
            return "קצר עם כובע" if wear_hat else "קצר בלי כובע"
    elif 15 < avg_temp < 22:
        return "ארוך עם כובע" if wear_hat else "ארוך בלי כובע"
    else:
        # below 15C degrees
        return "very cold, wear coat"


@register.filter("clothes_to_wear_all_week")
def clothes_to_wear_all_week(request):
    string_to_return =""
    API_handler = WeatherAPIWrapper()
    location, start_date, end_date = API_handler.extract_data_must(request)
    location_not_must, start_date_not_must, end_date_not_must = API_handler.extract_data_not_must(request)
    data_response_by_location_must = API_handler.get_location_weather_data(location).json()
    data_response_by_location_not_must = API_handler.get_location_weather_data(location_not_must)
    data_response_by_location_not_must_json = data_response_by_location_not_must.json()
    if data_response_by_location_not_must.status_code==200:
        date_different_not_must = end_date_not_must - start_date_not_must
        num_days_not_must = date_different_not_must.days + 1
        forecast_days_not_must = data_response_by_location_not_must_json["forecast"]["forecastday"]
    date_difference_must = end_date - start_date
    num_days_must = date_difference_must.days + 1
    forecast_days = data_response_by_location_must["forecast"]["forecastday"]
    string_to_return += f"for {location} wear:\n"
    for day in range(num_days_must):
        string_to_return +=f"יום {day+1}- " + clothes_to_wear_in_words(forecast_days[day]) +"\n"
    if data_response_by_location_not_must.status_code==200:
        string_to_return += f"for {location_not_must} wear:\n"
        for day in range(num_days_not_must):
            string_to_return += f"יום {day+num_days_must+1}- " + clothes_to_wear_in_words(forecast_days_not_must[day+num_days_must])+"\n"
    return string_to_return
