from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Booking, Seat, Team, CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_manager')


class SeatBookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Booking
        fields = ['seat', 'date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['seat'].queryset = Seat.objects.filter(team=user.team)



class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'total_seats']


class AddMembersForm(forms.Form):
    usernames = forms.CharField(widget=forms.Textarea, help_text='Enter the usernames of the existing users to add them to the team, separated by commas')

class AssignSeatsForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['total_seats']