from django import template
from datetime import datetime

register = template.Library()

days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
picture_paths_dict={'hot': "path", 'hot_with_hat': "path", 'cold': "path",'very_cold': "path",}

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
    if curr_temp > 25:
        return "images/man.png"
        #short clothes
    if 20 <= curr_temp < 25 and wind_speed_kph <= 15 and wear_hat:
        return "images/man.png"
        #short clothes
    elif 20 <= curr_temp < 25 and wind_speed_kph > 15 and wear_hat:
        return "images/man.png"
        #long clothes
    elif 15 < curr_temp < 20 and wear_hat:
        return "images/man.png"
        #wear long clothes
    else:
        return "images/sunny.png"






