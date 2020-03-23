from django.urls import path
from django.urls import include
from django.conf.urls import url
from BlogView import views as core_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # url(r'^register/$', core_views.signup, name='signup'),
   # url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
   #  url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
   #     core_views.activate, name='activate'), 
]

