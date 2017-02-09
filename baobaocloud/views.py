from django.http import HttpResponse
from django.shortcuts import render

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
