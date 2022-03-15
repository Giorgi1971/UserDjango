from django.contrib.auth.models import User


def users_links(request):
    links = User.objects.all()
    return dict(links=links)