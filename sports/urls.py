from django.urls import path, include
from . import views

urlpatterns = [
    path("test/", views.test, name="test"),
    path("play-by-play/", views.play_by_play, name="playbyplay"),
    path("",views.index,name="home"),
]