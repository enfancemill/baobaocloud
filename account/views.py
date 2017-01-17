from urlparse import urlparse

from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from baobaocloud.utils.decorators import nologin_required, method_required


@nologin_required()
@method_required('GET','POST')
def login(request):
    if request.method == 'GET':
        is_auth_failed = False
        interface = request.get_full_path()
        next_page = request.GET.get('next', reverse('index'))
        context = dict(is_auth_failed=is_auth_failed, interface=interface, next_page=next_page)
        return render(request, 'login.html', context)
    else:
        interface = request.get_full_path()
        next_page = request.POST.get('next', reverse('index'))
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(next_page)
        else:
            is_auth_failed = True
            context = dict(is_auth_failed=is_auth_failed, interface=interface, next_page=next_page)
            return render(request, 'login.html', context)

@login_required(redirect_field_name=None, login_url='/account/login/')
@method_required('GET')
def logout(request):
    referer = urlparse(request.META.get('HTTP_REFERER', reverse('index')))
    next_page = referer.path
    auth.logout(request)
    return HttpResponseRedirect(next_page)
