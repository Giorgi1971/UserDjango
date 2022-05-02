# This is a Twitter clone
## This project corresponds to the youtube tutorial:
### To use/configure it:
1. Clone the repository or download it as a zip.
git clone https://github.com/mundo-python/social_project.git

2. Create a virtual environment
python -m venv socialenv

3. Install dependencies/libraries in requirements.txt
pip install -r requirements.txt

4. Run the migrations.
python manage.py makemigrations python manage.py migrate

5. Create a super user.
python manage.py createsuperuser

6. Run the server.
python manage.py runserver




#This is for useradmin

We dont create User class. Only if necessary take it - from django.contrib.auth.models import User.
password save in 
* class UserCreateForm(forms.ModelForm):
*    password1 = forms.CharField(

#### href="?phrase={{ request.GET.phrase }}&page={{ page_obj.next_page_number }}"

# A Twitter-style post site has been built on User class

## Mainly used Django generic view

### Models:
* User class
* Post
* Twitter
* Like
* Comment
