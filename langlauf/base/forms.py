from django import forms
from django.forms import DateInput
from .models import Profile, Distance, Time


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['location', 'date_of_birth', 'bio', 'profile_picture']  # include profile_picture
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
        }

class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)

class DistanceForm(forms.ModelForm):
    class Meta:
        model = Distance
        fields = ("length", "full_name")

class TimeForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['distance', 'time_in_minutes', 'date']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }