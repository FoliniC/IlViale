from django.db import models
from newsletter.models import Subscription as ParentSubscription

from django.utils.translation import ugettext_lazy as _

class Subscription(ParentSubscription):
     localita_field = models.CharField(
        db_column='localita', max_length=30, blank=True, null=True,
        verbose_name=_('localita'), help_text=_('optional')
    )

from newsletter import *