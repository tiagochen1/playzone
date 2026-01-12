from django.db import models

# Create your models here.

class Campo(models.Model):
    nome = models.CharField(max_length=100)
    desporto = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome
