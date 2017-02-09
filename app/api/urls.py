from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^captcha/(\d+)/(\d+)/', views.captcha, name='captcha'),
]
