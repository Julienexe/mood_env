from django.shortcuts import render
from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TherapistAppointment
from .forms import ProfileUpdateForm
from Users.models import Profile 
from mood_trackers.models import User


#therpist home page
def home(request):
    profile = request.user.profile
    context = {"profile":profile}

    return render(request, 'therapists/home.html', context)

#appointments can view, accept and reschedule appointments
def appointments(request):
    appointments_ = TherapistAppointment.objects.filter(therapist=request.user.name).order_by('date_created')
    pending = TherapistAppointment.objects.filter(status="pending") 
    confirmed = TherapistAppointment.objects.filter(status="confirmed") 
    completed = TherapistAppointment.objects.filter(status="completed") 
    context = {'appointments':appointments_,'pending':pending,'confirmed':confirmed,'completed':completed}

    return render(request, 'therapists/appointments.html', context)

class MyProfile(LoginRequiredMixin, View):
    #class based view for a therapist to set a profile picture and have their role updated to therapist in their profile
    def get(self, request):
        #user_form = UserCreationForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            # 'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'therapists/profile.html', context)
    
    def post(self,request):
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        # if user_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():
            role=profile_form.save(commit=False)
            role.role=Profile.Roles.THERAPIST
            role.save()
            
            messages.success(request,'Your profile has been updated successfully')
            
            return redirect('therapists:home')
        else:
            context = {
                # 'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request,'Error updating your profile')
            
            return render(request, 'therapists/profile.html', context)
    




