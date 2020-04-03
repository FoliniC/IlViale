from django import template

register = template.Library()
 
@register.inclusion_tag('newsletter/message/newsletter-del-viale-della-formica/subscribe.html', takes_context=True)
def baseurl(context):
    """
    Return a BASE_URL template context for the current request.
    """
    base_url =  'a' +     context._current_scheme_host + 'b'
    return {'BASE_URL': base_url ,}