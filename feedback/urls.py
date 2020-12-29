from django.urls import include, path
from .views import feedback, savefeedback, listfeedback, perantara

urlpatterns = [
    path('', feedback, name='feedback'),
    path('savefeedback/', savefeedback),
    path('listfeedback/', listfeedback, name='listfeedback'),
    path('data/', perantara)
]