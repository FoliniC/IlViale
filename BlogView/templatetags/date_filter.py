import datetime
import locale

from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@stringfilter
def parse_date(date_string, format):
    """
    Return a datetime corresponding to date_string, parsed according to format.

    For example, to re-display a date string in another format::

        {{ "01/01/1970"|parse_date:"%m/%d/%Y"|date:"F jS, Y" }}

    """
    try:
        #locale.setlocale(locale.LC_TIME, 'it')
        return datetime.datetime.strptime(date_string, format)
    except ValueError:
        print ('Error converting date:' + date_string )
        return None

register.filter(parse_date)