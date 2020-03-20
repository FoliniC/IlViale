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
        
        fields = ('indirizzo_mail', 'nome', 'cognome', 'localita', 'consenso_privacy')
    def clean_consenso_privacy(self):
        consenso_privacy = self.cleaned_data['consenso_privacy']
        if not(consenso_privacy):
            raise forms.ValidationError("Devi selezionare il consenso alla privacy")
        return consenso_privacy