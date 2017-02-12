from django.core.urlresolvers import reverse
from django.shortcuts import render

from baobaologic.decorators import method_required


@method_required('GET')
def index(request):
    context = dict(user=request.user, api_login=reverse('login'),
                   api_logout=reverse('logout'), api_register=reverse('register'))
    return render(request, 'index.html', context)
