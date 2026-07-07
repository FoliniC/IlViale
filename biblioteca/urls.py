from django.urls import path
from . import views

urlpatterns = [
    path('', views.biblioteca_iframe, name='biblioteca_iframe'),  # /Biblioteca/ fa redirect
    path('iframe/', views.biblioteca_iframe, name='biblioteca_iframe'),  # /Biblioteca/iframe/ mostra iframe
    path('dona/', views.biblioteca_dona, name='biblioteca_dona'),  # /Biblioteca/dona/ mostra pagina de doação
    path('provaltellina_diretto/', views.biblioteca_dona, name='biblioteca_dona'),  # /Biblioteca/dona/ mostra pagina de doação
    path("provaltellina/", views.biblioteca_dona, name="biblioteca_diretto"), 
    #path("provaltellina/", views.provaltellina_prova, name="provaltellina_prova"), 
    path("provaltellina_prova/", views.provaltellina, name="provaltellina"), 
    path('robots.txt', views.RobotsTxtView, name="robots.txt"), 
]
