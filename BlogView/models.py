from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime  



class NewsletterRegistration(models.Model):
    
    # Fields
    indirizzo_mail = models.EmailField(max_length = 254,help_text='Inserisci l''email dove vuoi ricevere la newsletter',verbose_name='Inserisci il tuo indirizzo di email', unique=True) 
    nome = models.CharField(max_length=50,blank=True,help_text='se vuoi inserisci il tuo nome o un identificativo',verbose_name='Inserisci il tuo nome (facoltativo)')
    cognome = models.CharField(max_length=50,blank=True,help_text='se vuoi inserisci il tuo cognome',verbose_name='Inserisci il tuo cognome (facoltativo)')
    localita = models.CharField(max_length=50,blank=True,help_text='se vuoi inserisci la località',verbose_name='Inserisci il tuo comune (facoltativo)')
    consenso_privacy =  models.BooleanField(default=False,help_text='conferma di permetterci di registrare i dati inseriti')
    data_registrazione = models.DateTimeField(default=datetime.now, null=False, blank=True)
    data_revoca = models.DateTimeField(null=True, blank=True)
    # Metadata

    def __str__(self):
        return self.indirizzo_mail