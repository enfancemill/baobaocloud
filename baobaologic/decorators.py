from functools import wraps

from django.http import HttpResponseBadRequest, HttpResponseRedirect


def nologin_required(redirect_url='/'):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args):
            if request.user.is_authenticated():
                return HttpResponseRedirect(redirect_url)
            return func(request, *args)
        return wrapper
    return decorator


def method_required(*method):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args):
            if request.method not in method:
                return HttpResponseBadRequest()
            return func(request, *args)
        return wrapper
    return decorator
