from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.home,           name='home'),
    path('about/',                  views.about,          name='about'),
    path('services/',               views.services,       name='services'),
    path('services/<slug:slug>/',   views.service_detail, name='service_detail'),
    path('team/',                   views.team,           name='team'),
    path('join-us/',                views.join_us,        name='join_us'),
]