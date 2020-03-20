from django import forms

from django.forms import ModelForm
from BlogView.models import NewsletterRegistration

class RegisterForm(ModelForm):
    
    # Fields
    #indirizzo_mail = forms.EmailField(max_length=254, help_text='Inserisci il tuo indirizzo email')
    #nome = forms.CharField(max_length=100)
    # Metadata

    class Meta:
        model = NewsletterRegistration
        fields = ('indirizzo_mail', 'nome', )