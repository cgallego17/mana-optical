from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=40, unique=True)
    email = models.EmailField(blank=True)
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.nombre} ({self.telefono})'
