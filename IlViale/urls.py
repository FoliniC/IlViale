"""IlViale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
import logging

urlpatterns = [
    path('admin/', admin.site.urls),
    path('BlogView/', include('BlogView.urls')),
    path('info/', include('sito_statico.urls')),
    path('', RedirectView.as_view(url='/BlogView/', permanent=True)),
    url(r'^newsletter/', include('newsletter.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Amministrazione sito"
admin.site.site_title = "Amministrazione sito"
admin.site.index_title = "Amministrazione sito"

from django.conf import settings
from django.core.signals import request_started
from django.dispatch import receiver
from django.conf import settings


@receiver(request_started)
def my_request_started(sender, environ, **kwargs):
    logger = logging.getLogger("django")
    logger.warning(">>>>>>>>>>>Base url : " + settings.BASE_URL )
    if settings.BASE_URL=='':
        site = environ['HTTP_HOST']
        scheme = 'http' #if self.request.is_secure() else 'http'
        base_url_request = scheme + '://' + site
        if not ( base_url_request.find('.compute.amazonaws.com')>-1 and base_url_request.find('http://ec2')>-1):
            # double check if it's the right url
            logger.warning(">>>>>>>>>>>first:" + str(base_url_request.find('.compute.amazonaws.com')))
            logger.warning(">>>>>>>>>>>second:" + str(base_url_request.find('http://ec2')))
            logger.error("Base url didn\'t come from aws -> clear: " + base_url_request )
            base_url_request = ''    
        logger.warning('>>>>>>>>>>>Base Url:' + base_url_request)
        settings.BASE_URL = base_url_request 