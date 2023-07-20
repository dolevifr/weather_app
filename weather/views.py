from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class IndexPageView(View):
    def get(self, request):
        return render(request, 'index_page.html')

class ForcastInfo(View):
    def get(self,request):
        return render(request,'forcast_info.html')
