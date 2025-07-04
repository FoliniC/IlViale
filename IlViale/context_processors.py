# context_processors.py
from urllib.parse import urljoin
def canonical_url(request):
    return {
        'CANONICAL_URL': build_absolute_uri(request)
    }

# Assuming we have the request object
def build_absolute_uri(self, location=None):
    if not location:
        location = self.get_full_path()
    else:
        location = str(location)
    current_uri = '%s://%s%s' % (self.scheme, self.get_host(), self.path)
    query_params = self.GET.copy()

    # Remove the 'postToShow' attribute
    if 'postToShow' in query_params:
        del query_params['postToShow']

    # Reconstruct the URL without 'postToShow'
    location = self.path + '?' + query_params.urlencode() 
    return urljoin(current_uri,location)

def get_full_path(self):
    return '%s%s' % (self.path, self._get_query_string())

def _get_query_string(self):
    if self.META.get('QUERY_STRING'):
        return '?' + self.META['QUERY_STRING']
    return ''
