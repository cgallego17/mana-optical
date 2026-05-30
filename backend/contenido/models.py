from django.db import models


class HomeContent(models.Model):
    hero_titulo = models.CharField(max_length=160, blank=True)
    hero_subtitulo = models.TextField(blank=True)
    hero_cta_texto = models.CharField(max_length=80, blank=True)
    hero_cta_href = models.CharField(max_length=200, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return 'HomeContent'


class Banner(models.Model):
    titulo = models.CharField(max_length=160)
    subtitulo = models.TextField(blank=True)
    imagen_url = models.URLField(blank=True)
    href = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('orden', 'id')

    def __str__(self) -> str:
        return self.titulo


class Testimonio(models.Model):
    nombre = models.CharField(max_length=120)
    cargo = models.CharField(max_length=120, blank=True)
    texto = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('orden', 'id')

    def __str__(self) -> str:
        return self.nombre
