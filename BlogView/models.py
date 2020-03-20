from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class NewsletterRegistration(models.Model):
    
    # Fields
    indirizzo_mail = models.EmailField(max_length = 254,help_text='Inserisci l''email dove vuoi ricevere la newsletter',verbose_name='Inserisci il tuo indirizzo di email') 
    nome = models.CharField(max_length=50,blank=True,help_text='se vuoi inserisci il tuo nome o un identificativo',verbose_name='Inserisci il tuo nome (facoltativo)')
    cognome = models.CharField(max_length=50,blank=True,help_text='se vuoi inserisci il tuo cognome',verbose_name='Inserisci il tuo cognome (facoltativo)')
    localita = models.CharField(max_length=50,blank=True,help_text='se vuoi inserisci la località',verbose_name='Inserisci il tuo comune (facoltativo)')
    consenso_privacy =  models.BooleanField(default=False,help_text='conferma di permetterci di registrare i dati inseriti')
    # Metadata
