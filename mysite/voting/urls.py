from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('instructions/', views.instructions, name='instructions'),
    path('castVote/', views.cast_vote, name='castVote'),
    path('done/', views.done, name='done'),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('registerSuccess/', views.registerSuccess, name='registerSuccess'),
    path('checkVote/', views.checkVote, name='checkVote'),
    path('tally/', views.tally, name='tally'),
	path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('enterOTP/', views.enterOTP, name='enterOTP'),
    path('newPassword/', views.newPassword , name='newPassword'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout, name='logout')
]