from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from members.models import Profile


class SignupForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('avatar', 'bio', 'location')

class InvitationForm(forms.Form):
	email = forms.EmailField(max_length=200, help_text='Required')
