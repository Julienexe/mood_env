from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
import django.dispatch
#for emails
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site


from mood_trackers.forms import UserCreationForm, ProfileUpdateForm, MoodUpdate
from mood_trackers.models import User
from .models import Profile

#set up to register new users and verify their emails
def register(request):
    form = UserCreationForm()
    context = {'form':form}
    # if data is entered then....
    if request.method == 'POST':

        #the code below has a subject and message for the welcome email
        subject = 'Thank you for registering to our site'
        message = 'It means a lot to us, the Mood Tracker Community'
        email_from = settings.EMAIL_HOST_USER
        recipient_list=[request.POST['email']]

        #this is to send the email with the determined variables
        send_mail(subject,message,email_from, recipient_list)

        form = UserCreationForm(data=request.POST)
        if form.is_valid():

            # saving the form
            new_user = form.save()
            # here we log in the new user
            auth_login(request, new_user)
            # for convenience, we run to the home page after
            return HttpResponseRedirect(reverse('mood_trackers:home'))
        
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        # password = request.POST.get('password')


        # user = User(name=name, email=email, password=password)
        # user.save()
    else:
        # display a blank form
        form = UserCreationForm()
        return render(request, 'mood_trackers/register.html',context)
    return render(request, 'mood_trackers/register.html', context)

def login(request):
    # login page
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('Users:profile'))
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "mood_trackers/login.html", {"error": "Invalid email or password"})
    return render(request,'mood_trackers/login.html')

def therapist_login(request):
    # login page
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('therapists:home'))
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "Users/therapist_login.html", {"error": "Invalid email or password"})
    return render(request,'Users/therapist_login.html')



#for therapists
def therapist_register(request):
    form = UserCreationForm()
    context = {'form':form}
    # if data is entered then....
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():

            # saving the form
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email_from = settings.EMAIL_HOST_USER
            email = EmailMessage(
                mail_subject, message, email_from, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        # password = request.POST.get('password')


        # user = User(name=name, email=email, password=password)
        # user.save()
    else:
        # display a blank form
        form = UserCreationForm()
        return render(request, 'Users/therapist_register.html',context)
    return render(request, 'Users/therapist_register.html', context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        user.profile.role = Profile.Roles.THERAPIST
        auth_login(request, user)
        return HttpResponseRedirect(reverse('therapists:home'))
        
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def logout_view(request):
    logout(request)
    return redirect("mood_trackers:home")

#view function for viewing user profiles
def profile(request):
    profile = request.user.profile
    context = {"profile":profile}

    return render(request, 'Users/profile.html', context)

#class based view for the user profiles, to handle updates and viewing
class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        #user_form = UserCreationForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
        context = {
            # 'user_form': user_form,
            'profile_form': profile_form
        }
        
        return render(request, 'Users/profile_form.html', context)
    
    def post(self,request):
        # user_form = UserCreationForm(
        #     request.POST, 
        #     instance=request.user
        # )
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        # if user_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            
            messages.success(request,'Your profile has been updated successfully')
            
            return redirect('Users:profile')
        else:
            context = {
                # 'user_form': user_form,
                'profile_form': profile_form
            }
            messages.error(request,'Error updating your profile')
            
            return render(request, 'Users/profile_form.html', context)
        
def mood(request):
    form = MoodUpdate()
    profile = request.user.profile
    context = {'form':form, 'profile':profile}
    if request.method != 'POST':
        form = MoodUpdate()
        return render(request, 'Users/mood.html',context)  
    else:
        form = MoodUpdate(data=request.POST) 
        if form.is_valid():
            form.save()
            return render(request, 'Users/profile.html',context)
    return render(request, 'Users/mood.html', context)    
        
