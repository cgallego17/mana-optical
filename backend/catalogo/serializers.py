from rest_framework import serializers

from .models import Categoria, Marca, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre', 'slug')


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('id', 'nombre', 'slug')


class ProductoListSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    marca = MarcaSerializer()

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'slug',
            'descripcion',
            'precio',
            'precio_antes',
            'imagen_url',
            'categoria',
            'marca',
        )


class ProductoDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    marca = MarcaSerializer()

    class Meta:
        model = Producto
        fields = (
            'id',
            'nombre',
            'slug',
            'descripcion',
            'precio',
            'precio_antes',
            'imagen_url',
            'categoria',
            'marca',
            'creado_en',
        )
