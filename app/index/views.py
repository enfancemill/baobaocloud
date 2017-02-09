from django.shortcuts import render

from baobaologic.decorators import method_required

@method_required('GET')
def index(request):
    context = dict(user=request.user)
    return render(request, 'index.html', context)
