from django.contrib.auth.models import User
from django.db.models import *


def users_links(request):
    u_message = ''
    if request.method == 'GET':
        u_message = ""
    link = User.objects.annotate(dd=Count('author'))
    links = link.order_by('-dd')[0:3]
    sec_links = link.order_by('?')[0:3]
    return dict(links=links, sec_links=sec_links, u_message=u_message)
