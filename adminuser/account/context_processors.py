from django.contrib.auth.models import User


def users_links(request):
    return {'links':User.objects.all()}
    # links = User.objects.all()
    # return dict(links=links)