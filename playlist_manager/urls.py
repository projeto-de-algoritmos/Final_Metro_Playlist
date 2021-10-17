from django.contrib import admin
from django.urls import path

from playlist_manager import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
]
