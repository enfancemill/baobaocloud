from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    interface = request.get_full_path()
    if request.method == 'GET':
        is_auth_failed = False
        next_page = request.GET.get('next', reverse('index'))
        context = {'is_auth_failed': is_auth_failed, 'next_page': next_page, 'interface': interface}
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_page = request.POST.get('next', reverse('index'))
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect(next_page)
        else:
            is_auth_failed = True
            context = {'is_auth_failed': is_auth_failed, 'next_page': next_page, 'interface': interface}
            return render(request, 'login.html', context)
    else:
        return HttpResponseBadRequest()
