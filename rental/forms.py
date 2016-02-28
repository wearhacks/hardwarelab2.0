<<<<<<< HEAD

=======
>>>>>>> c86d5a2279e6a27aa18a7daf622690f744d08262
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm

from models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('first_name', 'last_name', 'email')
=======
        fields = ('first_name', 'last_name', 'email')
>>>>>>> c86d5a2279e6a27aa18a7daf622690f744d08262
