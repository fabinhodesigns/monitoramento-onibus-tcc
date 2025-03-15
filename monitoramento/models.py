from django.db import models

class Onibus(models.Model):
    numero = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Ônibus {self.id} - Localização atual'

class Parada(models.Model):
    nome = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.nome