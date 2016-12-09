from django.db import models

class Pessoa(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    lat = models.FloatField()
    long = models.FloatField()
    lat_max = models.FloatField()
    lat_min = models.FloatField()
    long_max = models.FloatField()
    long_min = models.FloatField()

    def __str__(self):
        return self.first_name
