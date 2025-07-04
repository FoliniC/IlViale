from django.urls import path
from . import views

app_name = 'turni_bar'
urlpatterns = [
    path('', views.home, name='home'),
]