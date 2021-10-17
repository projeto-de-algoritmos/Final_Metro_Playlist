from django.contrib import admin
from django.urls import path

from playlist_manager import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("attractions/", views.AttractionListView.as_view(), name="attraction-list"),
]
