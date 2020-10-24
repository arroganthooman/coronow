from django.http import request
from django.shortcuts import render

# Create your views here.
def covidstats(request):
    return render(request, "covidstats/covidstats.html")