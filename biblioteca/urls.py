from django.urls import path
from . import views

urlpatterns = [
    path('', views.biblioteca_redirect, name='biblioteca_redirect'),  # /Biblioteca/ fa redirect
    path('iframe/', views.biblioteca_iframe, name='biblioteca_iframe'),  # /Biblioteca/iframe/ mostra iframe
    path('dona/', views.biblioteca_dona, name='biblioteca_dona'),  # /Biblioteca/dona/ mostra pagina de doação
]