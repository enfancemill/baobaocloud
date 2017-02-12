from urlparse import urljoin, urlparse

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render

from baobaologic.config import ActMail
from baobaologic.decorators import method_required, nologin_required
from baobaologic.shortcuts import get_msg_code


@nologin_required()
@method_required('GET', 'POST')
def login(request):
    if request.method == 'GET':
        error_msg = None
        api_current = request.get_full_path()
        api_captcha = reverse('captcha')
        api_register = reverse('register')
        next_page = request.GET.get('next', reverse('index'))
        context = dict(error_msg=error_msg, next_page=next_page, api_current=api_current,
                       api_captcha=api_captcha, api_register=api_register)
        return render(request, 'login.html', context)
    else:
        api_current = request.get_full_path()
        api_captcha = reverse('captcha')
        api_register = reverse('register')
        next_page = request.POST.get('next', reverse('index'))
        verify_code = request.POST.get('verify_code', '')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.session['verify_code'] == verify_code.lower():
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                error_msg = get_msg_code(2)
        else:
            error_msg = get_msg_code(3)
        context = dict(error_msg=error_msg, next_page=next_page, api_current=api_current,
                       api_captcha=api_captcha, api_register=api_register)
        return render(request, 'login.html', context)


@login_required(redirect_field_name=None, login_url='/account/login/')
@method_required('GET')
def logout(request):
    referer = urlparse(request.META.get('HTTP_REFERER', reverse('index')))
    next_page = referer.path
    auth.logout(request)
    return HttpResponseRedirect(next_page)


@nologin_required()
@method_required('GET', 'POST')
def register(request):
    if request.method == 'GET':
        error_msg = None
        api_current = request.get_full_path()
        api_captcha = reverse('captcha')
        api_login = reverse('login')
        context = dict(error_msg=error_msg, api_current=api_current,
                       api_captcha=api_captcha, api_login=api_login)
        return render(request, 'register.html', context)
    else:
        api_current = request.get_full_path()
        api_captcha = reverse('captcha')
        api_login = reverse('login')
        api_activate = reverse('activate')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        verify_code = request.POST.get('verify_code', '')
        if request.session['verify_code'] == verify_code.lower():
            if not User.objects.filter(email=email):
                try:
                    user = User.objects.create_user(username, email, password, is_active=False)
                except IntegrityError:
                    error_msg = get_msg_code(4)
                else:
                    context = dict(is_activated=False, email=email, api_login=api_login,
                                   api_activate=api_activate)
                    return render(request, 'activate.html', context)
            else:
                error_msg = get_msg_code(5)
        else:
            error_msg = get_msg_code(3)
        context = dict(error_msg=error_msg, api_current=api_current,
                       api_captcha=api_captcha, api_login=api_login)
        return render(request, 'register.html', context)


@nologin_required()
@method_required('GET', 'POST')
def activate(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        api_login = reverse('login')
        User.objects.filter(email=email).update(is_active=True)
        context = dict(is_activated=True, api_login=api_login)
        return render(request, 'activate.html', context)
    else:
        email = request.POST.get('email')
        activate_url = urljoin(request.get_raw_uri(), '?email=%s' % email).encode('utf-8')
        send_mail(
            ActMail.subject,
            ActMail.content + activate_url,
            ActMail.source,
            [email],
            fail_silently=True,
        )
        return HttpResponse('ok')