from django.contrib.auth.models import User


def users_links(request):
    u_message = ''
    if request.method == 'GET':
        u_message = "POST METHOD"
    links = User.objects.all()
    return dict(links=links, u_message=u_message)
