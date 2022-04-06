from django.contrib import admin
from django.urls import path, include

import app.views

urlpatterns = [
    path('', views.index, name = "Landing"),
    path('parent', views.parentloginregister, name = 'Parent Portal') 
    #path('parenthome', views.)
]