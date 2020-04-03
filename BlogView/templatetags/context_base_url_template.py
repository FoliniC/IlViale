from django import template
from django.conf import settings

register = template.Library()
 
@register.inclusion_tag('base_url.html')
def baseurl():
    """
    Return a BASE_URL template context for the current request.
    """

    base_url =  settings.BASE_URL
    return {'BASE_URL': base_url ,}