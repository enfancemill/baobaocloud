from django.http import HttpResponse

from baobaologic.decorators import method_required
from baobaologic.shortcuts import get_random_string, get_string_imageflow

@method_required('GET')
def captcha(request, width, height):
    width = int(width)
    height = int(height)
    verify_code = get_random_string(length=4)
    verify_imageflow = get_string_imageflow(verify_code, width, height)
    request.session['verify_code'] = verify_code.lower()
    return HttpResponse(verify_imageflow, 'image/jpeg')
