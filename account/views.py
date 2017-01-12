from urlparse import urlparse

from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest


@csrf_exempt
def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'GET':
        is_auth_failed = False
        interface = request.get_full_path()
        next_page = request.GET.get('next', reverse('index'))
        context = dict(is_auth_failed=is_auth_failed, interface=interface, next_page=next_page)
        return render(request, 'login.html', context)
    elif request.method == 'POST':
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
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def logout(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    referer = urlparse(request.META.get('HTTP_REFERER', reverse('index')))
    next_page = referer.path
    auth.logout(request)
    return HttpResponseRedirect(next_page)
