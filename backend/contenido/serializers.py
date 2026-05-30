from rest_framework import serializers

from .models import Banner, HomeContent, Testimonio


class HomeContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeContent
        fields = (
            'hero_titulo',
            'hero_subtitulo',
            'hero_cta_texto',
            'hero_cta_href',
            'actualizado_en',
        )


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = (
            'id',
            'titulo',
            'subtitulo',
            'imagen_url',
            'href',
            'orden',
        )


class TestimonioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonio
        fields = (
            'id',
            'nombre',
            'cargo',
            'texto',
            'rating',
            'orden',
        )
