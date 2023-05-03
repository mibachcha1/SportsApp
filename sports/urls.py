from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
from . import routing

urlpatterns = [
    path("test/", views.test, name="test"),
    path('signup/', views.signup,name='signup'),
    path("schedule/", views.schedule, name="schedule"),
    path("search/", views.search, name="search"),
    path("boxscore/", views.boxscore, name="boxscore"),
    path("play-by-play/", views.play_by_play, name="playbyplay"),
    path("",views.index,name="home"),
    path('rooms/', views.rooms, name="rooms"),
    path('rooms/<slug:slug>/', views.room, name="room"),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login')
]