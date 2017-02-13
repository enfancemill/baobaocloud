from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/mail/$', views.register_mail, name='register_mail'),
    url(r'^register/activate/$', views.register_activate, name='register_activate'),
]
