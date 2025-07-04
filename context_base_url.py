from django import template
from django.conf import settings
from django.core.signals import request_started
from django.dispatch import receiver
from django.conf import settings
@receiver(request_started)
def my_request_started(sender, environ, **kwargs):
    if settings.BASE_URL=='':
        site = environ['HTTP_HOST']
        scheme = 'https' #if self.request.is_secure() else 'http'
        base_url_request = scheme + '://' + site
        settings.BASE_URL = base_url_request 
    

# register = template.Library()
 
# @register.inclusion_tag('base_url.html', takes_context=True)
# def baseurl(context):
#     """
#     Return a BASE_URL template context for the current request.
#     """
#     prova = '$$$'
#     base_url =  prova + 'aq' + settings.BASE_URL + 'bq' + context._current_scheme_host + 'c'

#     return {'BASE_URL': base_url ,}