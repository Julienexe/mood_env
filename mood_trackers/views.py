from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

from .models import User, Journal, Topic, Article
from .forms import JournalForm
from Users.models import Profile
from therapists.forms import Appointmentform

# views are created here

def index(request):
    # home page
    return render(request,'mood_trackers/index.html')

def journal(request):
    # journals for users to write their thoughts and feelings on a daily basis
    journal_entries = Journal.objects.filter(author = request.user).order_by('date_created')
    form = JournalForm()
    context = {"journal_entries":journal_entries}

    return render(request,'mood_trackers/journal.html', context)

def journal_entries(request):
    form = JournalForm()
    context = { "form":form}
    if request.method == 'POST':
        #save the data from the form into the database
        form = JournalForm(data=request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry = form.save()
            return redirect('mood_trackers:journal')
    else:
        #display a blank form
        form = JournalForm()
        return render(request, 'mood_trackers/journal_entries.html',context)
    return render(request,'mood_trackers/journal_entries.html', context)

def edit_journal(request, journal_id):
    journal= Journal.objects.get(id=journal_id)
    # form = JournalForm(instance=journal)
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = JournalForm(instance=journal)
    else:
        # POST data submitted; process data.
        form = JournalForm(instance=journal, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('mood_trackers:journal')
    context = {'journal':journal,'form':form}
    return render(request, 'mood_trackers/edit_journal.html',context)

#view function below was deprecated in favour of Users/profile.html    
def profile(request):
    # profile pages for user info
    return render(request,'mood_trackers/profile.html')

def resource_library(request):
    # resources for users such as activities, themes, etc
    topics = Topic.objects.all()
    context = {'topics':topics}
    return render(request,'mood_trackers/resource_library.html', context)

#view function that allows users to read individual resource articles
@login_required
def articles(request, topic_id):
    # here we pick the specific category/topic
    topic = Topic.objects.get(id = topic_id)

    # here we pick all articles related to that topic
    articles = topic.article_set.order_by('-date_added')

    context = {'articles':articles, 'topic':topic}
    return render(request,'mood_trackers/resource.html', context)


def therapy(request):
    # connect page that links users to their desired therapists
    therapists = Profile.objects.filter(role=Profile.Roles.THERAPIST)
    
    appointment = Appointmentform()

    context = {'therapists':therapists,'appointment':appointment}

    if request.method == 'POST' :
        appointment=Appointmentform(request.POST)
        if appointment.is_valid():
            appointment = appointment.save(commit=False)
            #code below is to set therapist and client variables before saving

            appointment.client = request.user.name
            #appointment.therapist = request.therapist.name

            #FORM IS SAVED WITH UPDATED DATA
            appointment = appointment.save()

        return redirect('mood_trackers:therapy')
    else:
        appointment= Appointmentform()

    return render(request,'mood_trackers/therapy.html', context)

