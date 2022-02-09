This is for useradmin

We dont create User class. Only if necessary take it - from django.contrib.auth.models import User.
password save in 
* class UserCreateForm(forms.ModelForm):
*    password1 = forms.CharField(
