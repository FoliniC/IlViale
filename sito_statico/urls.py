from django.urls import path
from django.urls import include
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('storia', TemplateView.as_view(template_name="sito_statico/storia.html")),
    path('mappa', TemplateView.as_view(template_name="sito_statico/mappa.html")),
    path('beni_architettonici', TemplateView.as_view(template_name="sito_statico/beni_architettonici.html")),
    
]

