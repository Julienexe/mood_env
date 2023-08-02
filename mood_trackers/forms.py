from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User ,Journal
from Users.models import Profile
 
EMOTIONS = [ ('happy','Happy'),
            ('sad','Sad'),
            ('angry','Angry'),
            ('confused','Confused'),
            ('fearful','Fearful'),
            ('disgusted','Disgusted'),
            ]


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email','name','password1','password2']

class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['title','content']

class ProfileUpdateForm(ModelForm):
    # moods = tuple(Profile.Moods.__dict__.values())

    # choices =forms.ChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Profile
        fields = ['avatar','mood']

class MoodUpdate(ModelForm):
    #choices =forms.ChoiceField(widget=forms.RadioSelect, choices=EMOTIONS)
    class Meta:
        model = Profile
        fields = ['mood']
        widgets = {'mood': forms.RadioSelect}
