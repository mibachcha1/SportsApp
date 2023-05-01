from django.urls import path, include
from . import views

urlpatterns = [
    path("test/", views.test, name="test"),
    path("schedule/", views.schedule, name="schedule"),
    path("search/", views.search, name="search"),
    path("boxscore/", views.boxscore, name="boxscore"),
    path("play-by-play/", views.play_by_play, name="playbyplay"),
    path("",views.index,name="home"),
]