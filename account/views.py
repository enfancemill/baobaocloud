from urlparse import urlparse

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render

from baobaocloud.utils.decorators import method_required, nologin_required
from baobaocloud.utils.shortcuts import get_msg_code


@nologin_required()
@method_required('GET', 'POST')
def login(request):
    if request.method == 'GET':
        error_msg = None
        interface = request.get_full_path()
        referer = urlparse(request.META.get('HTTP_REFERER', reverse('index')))
        next_page = request.GET.get('next', referer.path)
        context = dict(error_msg=error_msg, interface=interface, next_page=next_page)
        return render(request, 'login.html', context)
    else:
        interface = request.get_full_path()
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
        context = dict(error_msg=error_msg, interface=interface, next_page=next_page)
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
        interface = request.get_full_path()
        referer = urlparse(request.META.get('HTTP_REFERER', reverse('index')))
        next_page = request.GET.get('next', referer.path)
        context = dict(error_msg=error_msg, interface=interface, next_page=next_page)
        return render(request, 'register.html', context)
    else:
        interface = request.get_full_path()
        next_page = request.POST.get('next', reverse('index'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        verify_code = request.POST.get('verify_code', '')
        if request.session['verify_code'] == verify_code.lower():
            if not User.objects.filter(email=email):
                try:
                    user = User.objects.create_user(username, email, password)
                except IntegrityError:
                    error_msg = get_msg_code(4)
                else:
                    auth.login(request, user)
                    return HttpResponseRedirect(next_page)
            else:
                error_msg = get_msg_code(5)
        else:
            error_msg = get_msg_code(3)
        context = dict(error_msg=error_msg, interface=interface, next_page=next_page)
        return render(request, 'register.html', context)
