from django.contrib import admin
from .models import EmotionIdentification


@admin.register(EmotionIdentification)
class EmotionIdentificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_primary_emotion', 'intensity', 'created_at')
    list_filter = ('created_at', 'intensity', 'valence')
    search_fields = ('user__username', 'situation', 'personal_notes')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Informazioni Utente', {
            'fields': ('user', 'created_at')
        }),
        ('Situazione', {
            'fields': ('situation',)
        }),
        ('Risposte', {
            'fields': ('body_sensations', 'energy_type', 'triggers', 'impulses', 
                      'intensity', 'valence', 'duration')
        }),
        ('Risultati', {
            'fields': ('identified_emotions',)
        }),
        ('Note', {
            'fields': ('personal_notes',)
        }),
    )
