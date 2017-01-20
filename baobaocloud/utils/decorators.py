from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseRedirect


def nologin_required(redirect_url='/'):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if request.user.is_authenticated():
                return HttpResponseRedirect(redirect_url)
            return func(request)
        return wrapper
    return decorator

def method_required(*method):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if request.method not in method:
                return HttpResponseBadRequest()
            return func(request)
        return wrapper
    return decorator
