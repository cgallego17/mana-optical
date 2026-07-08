from datetime import date

from rest_framework import serializers

from clientes.models import Cliente

from .models import DiaExcepcion, HorarioAtencion, Reserva, Servicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = (
            'id',
            'nombre',
            'slug',
            'duracion_minutos',
            'dias_disponibles',
        )


class ServicioAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('id', 'nombre', 'slug', 'duracion_minutos', 'activo', 'dias_disponibles')

    def validate_dias_disponibles(self, value):
        if not isinstance(value, list) or not all(
            isinstance(d, int) and 0 <= d <= 6 for d in value
        ):
            raise serializers.ValidationError(
                'Debe ser una lista de días (0=Lunes … 6=Domingo).',
            )
        return sorted(set(value))


class HorarioAtencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioAtencion
        fields = ('id', 'dia_semana', 'abierto', 'hora_inicio', 'hora_fin')
        read_only_fields = ('dia_semana',)

    def validate(self, attrs):
        inicio = attrs.get('hora_inicio', getattr(self.instance, 'hora_inicio', None))
        fin = attrs.get('hora_fin', getattr(self.instance, 'hora_fin', None))
        if inicio and fin and inicio >= fin:
            raise serializers.ValidationError(
                {'hora_fin': 'La hora de fin debe ser posterior a la de inicio.'},
            )
        return attrs


class DiaExcepcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaExcepcion
        fields = ('id', 'fecha', 'abierto', 'hora_inicio', 'hora_fin', 'motivo')

    def validate(self, attrs):
        abierto = attrs.get('abierto', getattr(self.instance, 'abierto', False))
        inicio = attrs.get('hora_inicio', getattr(self.instance, 'hora_inicio', None))
        fin = attrs.get('hora_fin', getattr(self.instance, 'hora_fin', None))
        if abierto:
            if not inicio or not fin:
                raise serializers.ValidationError(
                    'Debes indicar hora de inicio y fin para una apertura especial.',
                )
            if inicio >= fin:
                raise serializers.ValidationError(
                    {'hora_fin': 'La hora de fin debe ser posterior a la de inicio.'},
                )
        else:
            attrs['hora_inicio'] = None
            attrs['hora_fin'] = None
        return attrs


class ReservaAdminSerializer(serializers.ModelSerializer):
    servicio_nombre = serializers.CharField(source='servicio.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)

    class Meta:
        model = Reserva
        fields = (
            'id',
            'servicio',
            'servicio_nombre',
            'cliente',
            'cliente_nombre',
            'fecha',
            'hora',
            'nombre',
            'telefono',
            'email',
            'notas',
            'estado',
            'creado_en',
        )
        read_only_fields = ('creado_en',)

    def validate(self, attrs):
        fecha = attrs.get('fecha', getattr(self.instance, 'fecha', None))
        hora = attrs.get('hora', getattr(self.instance, 'hora', None))
        estado = attrs.get('estado', getattr(self.instance, 'estado', Reserva.Estado.PENDIENTE))
        if fecha and hora and estado != Reserva.Estado.CANCELADA:
            qs = Reserva.objects.filter(fecha=fecha, hora=hora).exclude(
                estado=Reserva.Estado.CANCELADA,
            )
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'hora': 'Ese horario ya está reservado.'},
                )
        return attrs


class ReservaCreateSerializer(serializers.ModelSerializer):
    cliente_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model = Reserva
        fields = (
            'id',
            'servicio',
            'cliente_id',
            'fecha',
            'hora',
            'nombre',
            'telefono',
            'email',
            'notas',
        )

    def validate_fecha(self, value: date):
        if value < date.today():
            raise serializers.ValidationError(
                'La fecha no puede ser en el pasado.',
            )
        abierto, _, _ = HorarioAtencion.resolver_fecha(value)
        if not abierto:
            raise serializers.ValidationError('No hay atención ese día.')
        return value

    def validate(self, attrs):
        cliente_id = attrs.pop('cliente_id', None)
        if cliente_id is not None:
            try:
                attrs['cliente'] = Cliente.objects.get(pk=cliente_id)
            except Cliente.DoesNotExist as exc:
                raise serializers.ValidationError(
                    {
                        'cliente_id': 'Cliente no existe.',
                    }
                ) from exc
        else:
            telefono = (attrs.get('telefono') or '').strip()
            nombre = (attrs.get('nombre') or '').strip()
            if telefono:
                cliente, _ = Cliente.objects.get_or_create(
                    telefono=telefono,
                    defaults={
                        'nombre': nombre or telefono,
                        'email': attrs.get('email', ''),
                    },
                )
                attrs['cliente'] = cliente

        fecha = attrs.get('fecha')
        servicio = attrs.get('servicio')
        if fecha and servicio and servicio.dias_disponibles and fecha.weekday() not in servicio.dias_disponibles:
            raise serializers.ValidationError(
                {'fecha': 'El servicio no está disponible ese día.'},
            )

        hora = attrs.get('hora')
        if fecha and hora:
            exists = Reserva.objects.filter(
                fecha=fecha,
                hora=hora,
            ).exclude(
                estado=Reserva.Estado.CANCELADA,
            ).exists()
            if exists:
                raise serializers.ValidationError('Ese horario ya está reservado.')
        return attrs
