from rest_framework import serializers

from .models import Categoria, Marca, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ('id', 'nombre', 'slug', 'activa')
        extra_kwargs = {'activa': {'required': False}}


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = ('id', 'nombre', 'slug', 'activa')
        extra_kwargs = {'activa': {'required': False}}


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


class ProductoAdminSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    marca = MarcaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categoria',
        write_only=True,
        allow_null=True,
        required=False,
    )
    marca_id = serializers.PrimaryKeyRelatedField(
        queryset=Marca.objects.all(),
        source='marca',
        write_only=True,
        allow_null=True,
        required=False,
    )
    disponible = serializers.BooleanField(source='activo', required=False)

    class Meta:
        model = Producto
        fields = (
            'id', 'nombre', 'slug', 'descripcion',
            'precio', 'precio_antes', 'imagen_url',
            'categoria', 'categoria_id',
            'marca', 'marca_id',
            'disponible', 'creado_en',
        )
        read_only_fields = ('creado_en',)
