from django.urls import path
from .views import IndexPageView, ForcastInfo
#this file containes the different urls in my web app
urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('forecast/', ForcastInfo.as_view(), name='forecast')
]
