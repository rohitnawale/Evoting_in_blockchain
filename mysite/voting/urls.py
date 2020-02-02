from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('instructions/', views.instructions, name='instructions'),
    path('castVote/', views.cast_vote, name='castVote'),
    path('done/', views.done, name='done'),
    path('home/', views.home, name='home'),
]