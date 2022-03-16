This is for useradmin

We dont create User class. Only if necessary take it - from django.contrib.auth.models import User.
password save in 
* class UserCreateForm(forms.ModelForm):
*    password1 = forms.CharField(

### href="?phrase={{ request.GET.phrase }}&page={{ page_obj.next_page_number }}"
