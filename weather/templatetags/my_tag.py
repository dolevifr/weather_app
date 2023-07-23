from django import template
from datetime import datetime
from django.utils.safestring import mark_safe
register = template.Library()

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



