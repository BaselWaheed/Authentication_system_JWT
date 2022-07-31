from django.urls import path 

from . import views


urlpatterns = [
    path("profile/", views.UserProfileAPI.as_view(), name= 'profile'),


]