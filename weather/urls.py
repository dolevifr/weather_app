from django.urls import path
from .views import IndexPageView, ForcastInfo
urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('forecast/', ForcastInfo.as_view(), name='forecast')
]
