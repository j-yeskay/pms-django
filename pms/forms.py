from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.forms import widgets
from . models import Project, User


class UserRegistrationForm(UserCreationForm):
	username = forms.CharField(max_length = 255)
	firstname = forms.CharField(max_length = 255)
	lastname = forms.CharField(max_length = 255)
	email = forms.EmailField(max_length = 255)
	company = forms.CharField(max_length = 255)


	class Meta:
		model = User
		fields = ('username', 'firstname', 'lastname', 'email', 'company', 'password1', 'password2')





