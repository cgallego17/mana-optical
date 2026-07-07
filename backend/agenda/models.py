from datetime import time

from django.db import models

DIAS_SEMANA = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miércoles'),
    (3, 'Jueves'),
    (4, 'Viernes'),
    (5, 'Sábado'),
    (6, 'Domingo'),
)


class HorarioAtencion(models.Model):
    dia_semana = models.PositiveSmallIntegerField(choices=DIAS_SEMANA, unique=True)
    abierto = models.BooleanField(default=True)
    hora_inicio = models.TimeField(default=time(9, 0))
    hora_fin = models.TimeField(default=time(21, 0))

    class Meta:
        ordering = ['dia_semana']

    def __str__(self) -> str:
        return self.get_dia_semana_display()

    @classmethod
    def get_for_weekday(cls, weekday: int) -> 'HorarioAtencion':
        obj, _ = cls.objects.get_or_create(
            dia_semana=weekday,
            defaults={'abierto': weekday != 6},
        )
        return obj

    @classmethod
    def ensure_semana(cls) -> None:
        existentes = set(cls.objects.values_list('dia_semana', flat=True))
        faltantes = [d for d, _ in DIAS_SEMANA if d not in existentes]
        cls.objects.bulk_create([
            cls(dia_semana=d, abierto=d != 6) for d in faltantes
        ])


class Servicio(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    duracion_minutos = models.PositiveIntegerField(default=30)
    activo = models.BooleanField(default=True)
    # Días de la semana en que se ofrece el servicio (0=Lunes ... 6=Domingo).
    # Lista vacía significa "todos los días" (sujeto a las reglas globales de atención).
    dias_disponibles = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return self.nombre


class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        CONFIRMADA = 'confirmada', 'Confirmada'
        CANCELADA = 'cancelada', 'Cancelada'

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
    )
    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
    )
    fecha = models.DateField()
    hora = models.TimeField()
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    notas = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE,
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('fecha', 'hora'),
        )
        indexes = [
            models.Index(fields=['fecha', 'hora']),
        ]

    def __str__(self) -> str:
        return f"{self.fecha} {self.hora} - {self.nombre}"
