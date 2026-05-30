from rest_framework import serializers

from django.utils import timezone

from .models import CategoriaBlog, Post


class CategoriaBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaBlog
        fields = (
            'id',
            'nombre',
            'slug',
        )


class PostListSerializer(serializers.ModelSerializer):
    categoria = CategoriaBlogSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'titulo',
            'slug',
            'extracto',
            'imagen_url',
            'publicado_en',
            'creado_en',
            'categoria',
        )


class PostDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaBlogSerializer()

    class Meta:
        model = Post
        fields = (
            'id',
            'titulo',
            'slug',
            'extracto',
            'contenido',
            'imagen_url',
            'publicado_en',
            'creado_en',
            'categoria',
        )


class PostAdminSerializer(serializers.ModelSerializer):
    categoria = CategoriaBlogSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        source='categoria',
        queryset=CategoriaBlog.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'titulo',
            'slug',
            'extracto',
            'contenido',
            'imagen_url',
            'publicado',
            'publicado_en',
            'creado_en',
            'categoria',
            'categoria_id',
        )

    def _apply_publicado_en(
        self,
        instance: Post,
        validated_data: dict,
    ) -> None:
        publicado = validated_data.get('publicado', instance.publicado)
        publicado_en = validated_data.get(
            'publicado_en',
            instance.publicado_en,
        )
        if publicado and not publicado_en:
            validated_data['publicado_en'] = timezone.now()

    def create(self, validated_data):
        dummy = Post(
            **{
                k: v
                for k, v in validated_data.items()
                if k in {
                    'publicado',
                    'publicado_en',
                }
            }
        )
        self._apply_publicado_en(dummy, validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self._apply_publicado_en(instance, validated_data)
        return super().update(instance, validated_data)
