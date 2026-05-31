from datetime import date

from rest_framework import serializers

from clientes.models import Cliente

from .models import Reserva, Servicio


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = (
            'id',
            'nombre',
            'slug',
            'duracion_minutos',
        )


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
        if value.weekday() == 6:
            raise serializers.ValidationError('No hay atención los domingos.')
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
