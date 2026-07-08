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

    @classmethod
    def resolver_fecha(cls, fecha):
        """Devuelve (abierto, hora_inicio, hora_fin) para una fecha puntual.
        Da prioridad a una excepción de calendario sobre el horario semanal."""
        excepcion = DiaExcepcion.objects.filter(fecha=fecha).first()
        if excepcion:
            if not excepcion.abierto:
                return False, None, None
            return True, excepcion.hora_inicio, excepcion.hora_fin
        horario = cls.get_for_weekday(fecha.weekday())
        if not horario.abierto:
            return False, None, None
        return True, horario.hora_inicio, horario.hora_fin


class DiaExcepcion(models.Model):
    """Excepción de calendario que anula el horario semanal en una fecha
    concreta: festivos/cierres (abierto=False) o aperturas extra (abierto=True)."""
    fecha = models.DateField(unique=True)
    abierto = models.BooleanField(default=False)
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    motivo = models.CharField(max_length=140, blank=True)

    class Meta:
        ordering = ['fecha']

    def __str__(self) -> str:
        estado = (
            f"{self.hora_inicio}-{self.hora_fin}" if self.abierto else 'cerrado'
        )
        return f"{self.fecha} ({estado})"


class Servicio(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    duracion_minutos = models.PositiveIntegerField(default=30)
    activo = models.BooleanField(default=True)
    # Días de la semana en que se ofrece el servicio (0=Lunes ... 6=Domingo).
    # Lista vacía significa "todos los días" (sujeto a las reglas globales de atención).
    dias_disponibles = models.JSONField(default=list, blank=True)
    # Horario propio por día: {"0": {"inicio": "09:00", "fin": "13:00"}, ...}.
    # Un día sin entrada aquí usa el horario/excepción global de ese día.
    horarios_dias = models.JSONField(default=dict, blank=True)
    # Rango de fechas en que el servicio puede reservarse (ambas opcionales;
    # vacías = sin límite de vigencia).
    vigencia_desde = models.DateField(null=True, blank=True)
    vigencia_hasta = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nombre

    def horario_para_dia(self, weekday: int):
        """Devuelve (hora_inicio, hora_fin) propios del servicio para ese día
        de la semana, o (None, None) si ese día no tiene horario propio."""
        entry = (self.horarios_dias or {}).get(str(weekday))
        if not entry:
            return None, None
        return time.fromisoformat(entry['inicio']), time.fromisoformat(entry['fin'])

    def vigente_en(self, fecha) -> bool:
        if self.vigencia_desde and fecha < self.vigencia_desde:
            return False
        if self.vigencia_hasta and fecha > self.vigencia_hasta:
            return False
        return True


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
        constraints = [
            # Un mismo horario solo se bloquea mientras la reserva siga activa;
            # si se cancela, el turno vuelve a quedar libre para reagendar.
            models.UniqueConstraint(
                fields=['fecha', 'hora'],
                condition=~models.Q(estado='cancelada'),
                name='reserva_activa_unica_por_fecha_hora',
            ),
        ]
        indexes = [
            models.Index(fields=['fecha', 'hora']),
        ]

    def __str__(self) -> str:
        return f"{self.fecha} {self.hora} - {self.nombre}"
