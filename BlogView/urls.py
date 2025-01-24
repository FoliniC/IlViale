from django.urls import path
#from django.urls import include
#from django.urls import re_path
from . import views
# urls.py
from . import viewsFile


urlpatterns = [
    path('', views.index, name='index'),
    path('pro', views.index, name='index'),
    path('directory/<path:path>/', viewsFile.list_directory, name='list_directory'),
    path('directory/', viewsFile.list_directory, name='list_directory'),
    # re_path(r'^register/$', core_views.signup, name='sign up'),
   # re_path(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
   #  re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
   #     core_views.activate, name='activate'), 
]

