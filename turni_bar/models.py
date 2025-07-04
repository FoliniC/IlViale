from django.db import models
from django.contrib.auth.models import User

class Gruppo(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    creato_da = models.ForeignKey(User, on_delete=models.CASCADE)
    data_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Barista(models.Model):
    nome = models.CharField(max_length=100)
    gruppo = models.ForeignKey(Gruppo, on_delete=models.CASCADE)
    turni_effettuati = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.gruppo.nome})"

class Turno(models.Model):
    barista = models.ForeignKey(Barista, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-data']