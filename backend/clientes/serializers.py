from rest_framework import serializers

from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = (
            'id',
            'nombre',
            'telefono',
            'email',
            'notas',
            'creado_en',
        )
        read_only_fields = ('id', 'creado_en')
