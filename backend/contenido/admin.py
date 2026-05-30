from django.contrib import admin

from .models import Banner, HomeContent, Testimonio


@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ('hero_titulo', 'actualizado_en')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'activo')
    list_filter = ('activo',)
    search_fields = ('titulo', 'subtitulo')
    ordering = ('orden', 'id')


@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rating', 'orden', 'activo')
    list_filter = ('activo', 'rating')
    search_fields = ('nombre', 'cargo', 'texto')
    ordering = ('orden', 'id')
