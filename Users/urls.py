#here we have urls for the main app
from . import views
from django.urls import path

app_name = 'Users'
#this is used to identify our application in django's url system.\

urlpatterns = [
    #login and logout pages which will be shifted to user app
    path('login/', views.login, name='login'),
    # register page for users
    path('register', views.register, name='register'),
    #register page for therapists
    path('therapist_register', views.therapist_register, name='register_therapist' ),
    #path for therapist login page
    path('therapist_login/',views.therapist_login, name = 'therapist_login'),
    #logout page
    path('logout/', views.logout_view, name='logout'),
    #path to update profile page
    path('update_profile/',views.MyProfile.as_view(), name='update_profile'),
    #path to profile page
    path("profile/", views.profile, name="profile"),
    #path to mood page
    path('mood/', views.mood, name='mood'),
    #email verification
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
]