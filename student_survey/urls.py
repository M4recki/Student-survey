"""
URL configuration for student_survey project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('survey/', views.survey, name='survey'),
    path('take_survey/<int:survey_id>/', views.take_survey, name='take_survey'),
    path('create_survey/', views.create_survey, name='create_survey'),
    path('manage_surveys/', views.manage_surveys, name='manage_surveys'),
    path('admin_stats/', views.admin_stats, name='admin_stats'),
    path('about/', views.about, name='about'),
]
