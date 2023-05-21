from . import views
from django.urls import path

urlpatterns = [
    path('',views.base),
    path('now/', views.now),
    path('news/',views.news),
    path('films/', views.films),
    path('serials/', views.serials),
    path('myltfilms/', views.myltfilms),
    path('tele/', views.tele),
    path('anime/', views.anime),
    path('ajax/', views.ozvuchka),
    path('film/',views.film)
]
