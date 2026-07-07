from django import forms
from django.apps import apps

class EmotionIdentificationForm(forms.Form):
    """Form per la raccolta dati dell'identificazione emotiva"""
    
    situation = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Descrivi brevemente la situazione o l\'evento...'
        }),
        label='Descrivi la situazione'
    )
    
    body_sensations = forms.MultipleChoiceField(
        choices=[
            ('chest', 'Petto/cuore (oppressione, battito accelerato)'),
            ('stomach', 'Stomaco/pancia (nodo, farfalle, tensione)'),
            ('throat', 'Gola (chiusa, nodo)'),
            ('head', 'Testa (pressione, confusione)'),
            ('muscles', 'Muscoli (tensione, rigidità)'),
            ('whole_body', 'Tutto il corpo (stanchezza, pesantezza)'),
            ('none', 'Non la sento fisicamente'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Dove senti questa emozione nel corpo?',
        required=False
    )
    
    energy_type = forms.ChoiceField(
        choices=[
            ('', '-- Seleziona --'),
            ('outward', 'Energia verso l\'esterno (voglia di agire, parlare, muovermi)'),
            ('inward', 'Energia verso l\'interno (voglia di ritirarmi, chiudermi)'),
            ('blocked', 'Energia bloccata (vorrei agire ma non riesco)'),
            ('low', 'Poca o nessuna energia (apatia, stanchezza)'),
        ],
        label='Che tipo di energia senti?'
    )
    
    triggers = forms.MultipleChoiceField(
        choices=[
            ('loss', 'Una perdita o mancanza di qualcosa'),
            ('threat', 'Una minaccia o pericolo (reale o percepito)'),
            ('obstacle', 'Un ostacolo o impedimento'),
            ('injustice', 'Un\'ingiustizia o qualcosa di sbagliato'),
            ('pleasant', 'Qualcosa di piacevole o desiderabile'),
            ('benefit', 'Un beneficio ricevuto da qualcuno'),
            ('mistake', 'Una mia mancanza o errore'),
            ('unexpected', 'Qualcosa di inaspettato'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Cosa ha scatenato questa emozione?',
        required=False
    )
    
    impulses = forms.MultipleChoiceField(
        choices=[
            ('escape', 'Allontanarmi o scappare'),
            ('attack', 'Attaccare o cambiare la situazione'),
            ('withdraw', 'Chiudermi o isolarmi'),
            ('approach', 'Avvicinarmi o condividere'),
            ('avoid', 'Evitare o rimandare'),
            ('solve', 'Risolvere o sistemare'),
            ('blocked', 'Niente, sono bloccato/a'),
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Cosa ti viene voglia di fare?',
        required=False
    )
    
    intensity = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=5,
        widget=forms.NumberInput(attrs={'type': 'range'}),
        label='Intensità (1-10)'
    )
    
    valence = forms.ChoiceField(
        choices=[
            ('', '-- Seleziona --'),
            ('positive', 'Principalmente piacevole/positiva'),
            ('negative', 'Principalmente spiacevole/negativa'),
            ('neutral', 'Neutra o mista'),
        ],
        label='Come la descriveresti?'
    )
    
    duration = forms.ChoiceField(
        choices=[
            ('', '-- Seleziona --'),
            ('recent', 'È appena iniziata (minuti/ore)'),
            ('days', 'Da qualche giorno'),
            ('weeks', 'Da settimane o più'),
            ('recurring', 'È ricorrente, va e viene'),
        ],
        label='Da quanto tempo la provi?'
    )


class PersonalNotesForm(forms.ModelForm):
    """Form per aggiungere note personali a un'identificazione esistente"""
    
    class Meta:
        fields = ['personal_notes']
        widgets = {
            'personal_notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Aggiungi note, riflessioni o aggiornamenti...'
            })
        }

    def __init__(self, *args, **kwargs):
        # Import lazy del modello per evitare import circolari
        EmotionIdentification = apps.get_model('emotion_tracker', 'EmotionIdentification')
        self._meta.model = EmotionIdentification
        super().__init__(*args, **kwargs)