#here we have urls for the main app
from . import views
from django.urls import path

app_name = 'mood_trackers'
#this is used to identify our application in django's url system.\

urlpatterns = [
    #home page
    path('', views.index, name='home'),

    #login and logout pages which will be shifted to user app
   # path('login/', views.login, name='login'),
    # register page for users
   # path('register', views.register, name='register'),
    #logout page
   # path('logout/', views.logout_view, name='logout'),

    # page for the users to view their journals
    path('journal/', views.journal, name='journal'),
    #page for adding new journals
    path('add_entry/', views.journal_entries, name='add_entry'),
    # page for users to edit their journals
    path('edit_journal/<journal_id>', views.edit_journal, name="edit_journal" ),    
    # page for user profiles
    path('profile/',views.profile, name="profile"),
    # page for the resource library
    path("resource_library/", views.resource_library, name="resource_library"),
    #page for therapy
    path('therapy/', views.therapy, name='therapy'),
    # view path for an individual page
    path('topic/<topic_id>', views.articles, name= 'topic'),
]