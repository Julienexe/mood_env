from . import views
from django.urls import path

app_name = 'therapists'

urlpatterns = [
    #login and logout pages which will be shifted to user app
    path("home", views.home, name="home"),
    #path to appointments page
    path('appointments/',views.appointments, name='appointments'),
    #path for the myprofile classbased view
    path('profile/', views.MyProfile.as_view(), name = 'profile'),


]