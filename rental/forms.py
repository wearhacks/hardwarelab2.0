from django import forms
from models import UserProfile

class UserSettingsForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['user.first_name', 'user.last_name', 'phone_number', 'user.email']
