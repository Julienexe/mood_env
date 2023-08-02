from django.forms import ModelForm
from django import forms
from Users.models import Profile
from .models import TherapistAppointment

class ProfileUpdateForm(ModelForm):
    # moods = tuple(Profile.Moods.__dict__.values())

    # choices =forms.ChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Profile
        fields = ['avatar','role']


class Appointmentform(ModelForm):
    class Meta:
        model = TherapistAppointment
        fields = ['therapist','date','duration','time']
        widgets = {'date': forms.DateInput,
                   'duration':forms.TimeInput,
                   'time' : forms.TimeInput,
                   }
