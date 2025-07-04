from django.contrib import admin
from .models import Gruppo, Barista, Turno

@admin.register(Gruppo)
class GruppoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_creazione', 'creato_da')  # Usa data_creazione invece di creato_il
    list_filter = ('data_creazione',)

@admin.register(Barista)
class BaristaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'gruppo', 'turni_effettuati')
    list_filter = ('gruppo',)

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('barista', 'data')