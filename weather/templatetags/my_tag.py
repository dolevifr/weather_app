from django import template
from datetime import datetime
from django.utils.safestring import mark_safe

register = template.Library()

days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
picture_paths_dict = {'hot': "path", 'hot_with_hat': "path", 'cold': "path",'very_cold': "path",}
#need to change the paths to the dict from clothes to wear

@register.filter("epoch_to_day")
def epoch_to_day(epoch_timestamp):
    dt_object = datetime.fromtimestamp(epoch_timestamp)
    day_of_week_number = dt_object.weekday()
    return days_of_week[day_of_week_number]


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
            return "images/summer_cap.png" if wear_hat else "images/summer.png"
    if 20 <= curr_temp < 25 and wind_speed_kph <= 15:
        return "images/summer_cap.png" if wear_hat else "images/summer.png"
        #short clothes
    elif 20 <= curr_temp < 25 and wind_speed_kph > 15:
        return "images/fall_cap.png" if wear_hat else "images/fall.png"
        #long clothes
    elif 15 < curr_temp < 20:
        return "images/fall.png"
    else:
        #below 15C degrees
        return "images/winter.png"


@register.filter("weather_icon")
def weather_icon(day_data):
    single_day = day_data["day"] #API doesnt provide daily cloud percentage, for next time need to choose a better API
    chance_of_rain = single_day["daily_chance_of_rain"]
    if chance_of_rain > 20:
        return "fa-solid fa-cloud-rain"
    else:
        return "fa-solid fa-cloud-sun"



