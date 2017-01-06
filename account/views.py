from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'is_authentication_required': False})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return render(request, 'login.html', {'is_authentication_required': True, 'is_authentication_succeed': True})
        else:
            return render(request, 'login.html', {'is_authentication_required': True, 'is_authentication_succeed': False})
    else:
        return HttpResponseBadRequest()
