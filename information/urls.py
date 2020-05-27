from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),  # /information
    path('selectCountry', views.select_country)  # /information/selectCountry
]
