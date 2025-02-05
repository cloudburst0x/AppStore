"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('parent', app.views.parentloginregister, name='Parents Portal'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('parentcreatejob', app.views.parentcreatejob, name='parentcreatejob'),
    #path('jobs', app.views.JobsListView.as_view(), name = 'Jobs Portal'), #HTML Name: <app>_list.html
    #path('job/new/', app.views.CreateJobs.as_view(), name = 'Create Jobs Form') #HTML Name: <app>_form.html
]
