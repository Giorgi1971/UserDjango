# UserDjango

# User class

##### რეპოზიტორი შექმნილია მომხმარებლის კლასის სხვადასხვა ვარიანტების შესანახად და სამართავად
#### The repository is designed to store and manage different variants of the User class

> ## List User Class Types. All types has Readme.md
## * 1 - adminUser: 
forms.py: class UserCreateForm(forms.ModelForm): 
* def clean_password2
* def _post_clean
* def save
models.py, admin.py - ცარიელი
urls.py და  views.py: register, login, logout.

## * 2 - SimpleUser: 
forms.py: 
class UserCreateForm(**UserCreationForm**):
    class Meta:
        model = get_user_model()
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Dispay Name'
models.py, admin.py - ცარიელი
urls.py:     
  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  path('signup/', views.SignUp.as_view() , name='signup'),
views.py:
  class SignUp(CreateView):

