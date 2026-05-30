from django.db import models


class CategoriaBlog(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoría Blog'
        verbose_name_plural = 'Categorías Blog'

    def __str__(self) -> str:
        return self.nombre


class Post(models.Model):
    categoria = models.ForeignKey(
        CategoriaBlog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    titulo = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    extracto = models.TextField(blank=True)
    contenido = models.TextField(blank=True)
    imagen_url = models.URLField(blank=True)
    publicado = models.BooleanField(default=False)
    publicado_en = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-publicado_en', '-creado_en')

    def __str__(self) -> str:
        return self.titulo
