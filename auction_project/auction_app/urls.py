from django.conf.urls import url
from auction_app import views
from django.urls import path

urlpatterns =[
    path('index', views.index, name='index'),

]