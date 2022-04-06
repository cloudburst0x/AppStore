from django.contrib import admin
from django.urls import path, include


import app.views

urlpatterns = [
    path('test', app.views.index, name = 'test')

]