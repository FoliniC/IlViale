from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmotionIdentification(models.Model):
    """Modello per salvare le identificazioni emotive"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_identifications')
    created_at = models.DateTimeField(default=timezone.now)
    
    # Situazione descritta
    situation = models.TextField(verbose_name="Situazione")
    
    # Risposte alle domande (salvate come JSON per flessibilità)
    body_sensations = models.JSONField(default=list, verbose_name="Sensazioni corporee")
    energy_type = models.CharField(max_length=200, blank=True, verbose_name="Tipo di energia")
    triggers = models.JSONField(default=list, verbose_name="Fattori scatenanti")
    impulses = models.JSONField(default=list, verbose_name="Impulsi all'azione")
    intensity = models.IntegerField(default=5, verbose_name="Intensità (1-10)")
    valence = models.CharField(max_length=100, blank=True, verbose_name="Valenza emotiva")
    duration = models.CharField(max_length=100, blank=True, verbose_name="Durata")
    
    # Risultati dell'analisi
    identified_emotions = models.JSONField(default=list, verbose_name="Emozioni identificate")
    
    # Note personali aggiunte successivamente
    personal_notes = models.TextField(blank=True, verbose_name="Note personali")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Identificazione Emotiva"
        verbose_name_plural = "Identificazioni Emotive"
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
    
    def get_primary_emotion(self):
        """Restituisce l'emozione principale identificata"""
        if self.identified_emotions and len(self.identified_emotions) > 0:
            return self.identified_emotions[0].get('emotion', 'Non identificata')
        return 'Non identificata'
