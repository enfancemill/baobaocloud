from urlparse import urljoin

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render

from baobaocloud.settings import EMAIL_HOST_USER
from baobaocloud.utils.const import ActMail
from baobaocloud.utils.decorators import method_required
from baobaocloud.utils.shortcuts import get_random_string, get_string_imageflow

@method_required('GET')
def index(request):
    context = dict(user=request.user)
    return render(request, 'index.html', context)

@method_required('GET')
def verify(request, width, height):
    width = int(width)
    height = int(height)
    verify_code = get_random_string(length=4)
    verify_imageflow = get_string_imageflow(verify_code, width, height)
    request.session['verify_code'] = verify_code.lower()
    return HttpResponse(verify_imageflow, 'image/jpeg')

@method_required('GET')
def actmail(request):
    email = request.GET.get('email')
    user = User.objects.get(email=email)
    user.is_active = True
    user.save()
    context = dict(is_active=True)
    return render(request, 'active.html', context)

@method_required('GET')
def send_actmail(request):
    email = request.GET.get('email')
    actmail_url = urljoin('http://' + request.get_host() + reverse('actmail'), '?email=%s' % email)
    send_mail(
        ActMail.subject,
        ActMail.content + actmail_url.encode('utf-8'),
        EMAIL_HOST_USER,
        [email],
    )
    return HttpResponse('ok')
