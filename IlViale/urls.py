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
import concurrent_log_handler

# # First import the register function.
# from sitetree.sitetreeapp import register_items_hook
# # The following function will be used as items processor.
# def my_items_processor(tree_items, tree_sender, context):
#     # Suppose we want to process only menu child items.
#     if tree_sender == 'menu.children':
#         # Lets add 'Hooked: ' to resolved titles of every item.
#         for item in tree_items:
#             item.title_resolved = 'Hooked: %s' % item.title_resolved
#     # Return items list mutated or not.
#     return tree_items

# # And we register items processor.
# register_items_hook(my_items_processor)        

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

import os

@receiver(request_started)
def my_request_started(sender, environ, **kwargs):
    
    logger = logging.getLogger("django")
    logger.warning("new request")
    #logger.warning(">>>>>>>>>>>Base url : " + settings.BASE_URL + "<<<" )
    if settings.BASE_URL=='':
        site = environ['HTTP_HOST']
        scheme = 'http' #if self.request.is_secure() else 'http'
        base_url_request = scheme + '://' + site
        #logger.warning('>>>>>>>>>>>Check Base Url:' + base_url_request)
        server_type = ''
        try:
             server_type = os.environ["SERVER_TYPE"]
        except :
            logger.exception("server_type not found > prod")
            server_type = 'PROD'
        logger.warning('>>>>>>>>>>>SERVER_TYPE' + server_type )
        if not (server_type=='DEVHOME' or server_type=='DEV') and not (base_url_request.find('http://VialeFormica.it')>-1 or base_url_request.lower().find('http://vialeformica.org')>-1 or ( base_url_request.find('.compute.amazonaws.com')>-1 and base_url_request.find('http://ec2')>-1)):
            # double check if it's the right url
            logger.warning(">>>>>>>>>>>first:" + str(base_url_request.find('.compute.amazonaws.com')))
            logger.warning(">>>>>>>>>>>second:" + str(base_url_request.find('http://ec2')))
            logger.error("Base url didn\'t come from AWS -> clear: " + base_url_request )
            base_url_request = ''    
            raise Exception("Base url didn\'t come from AWS -> clear: " + base_url_request)
        logger.warning('>>>>>>>>>>>Error Base Url:' + base_url_request)
        settings.BASE_URL = base_url_request 


