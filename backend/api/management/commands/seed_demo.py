from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from agenda.models import Servicio
from catalogo.models import Categoria, Marca, Producto


class Command(BaseCommand):
    help = 'Crea datos de ejemplo (SQLite) para desarrollo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Si está presente, recrea/actualiza registros existentes.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = bool(options.get('force'))

        categoria_nombre = 'Monturas'
        categoria_slug = slugify(categoria_nombre)
        categoria, _ = Categoria.objects.get_or_create(
            slug=categoria_slug,
            defaults={'nombre': categoria_nombre, 'activa': True},
        )
        if force and categoria.nombre != categoria_nombre:
            categoria.nombre = categoria_nombre
            categoria.activa = True
            categoria.save(update_fields=['nombre', 'activa'])

        marca_nombre = 'Ray-Ban'
        marca_slug = slugify(marca_nombre)
        marca, _ = Marca.objects.get_or_create(
            slug=marca_slug,
            defaults={'nombre': marca_nombre, 'activa': True},
        )
        if force and marca.nombre != marca_nombre:
            marca.nombre = marca_nombre
            marca.activa = True
            marca.save(update_fields=['nombre', 'activa'])

        productos = [
            {
                'nombre': 'Montura clásica negra',
                'slug': 'montura-clasica-negra',
                'descripcion': 'Montura ligera y elegante para uso diario.',
                'precio': '299000.00',
                'precio_antes': '349000.00',
                'imagen_url': '',
            },
            {
                'nombre': 'Montura premium dorada',
                'slug': 'montura-premium-dorada',
                'descripcion': 'Acabado premium con estilo sofisticado.',
                'precio': '459000.00',
                'precio_antes': None,
                'imagen_url': '',
            },
        ]

        for p in productos:
            producto, created = Producto.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'nombre': p['nombre'],
                    'categoria': categoria,
                    'marca': marca,
                    'descripcion': p['descripcion'],
                    'precio': p['precio'],
                    'precio_antes': p['precio_antes'],
                    'imagen_url': p['imagen_url'],
                    'activo': True,
                },
            )
            if force and not created:
                producto.nombre = p['nombre']
                producto.categoria = categoria
                producto.marca = marca
                producto.descripcion = p['descripcion']
                producto.precio = p['precio']
                producto.precio_antes = p['precio_antes']
                producto.imagen_url = p['imagen_url']
                producto.activo = True
                producto.save()

        servicio_nombre = 'Examen visual completo'
        servicio_slug = slugify(servicio_nombre)
        servicio, _ = Servicio.objects.get_or_create(
            slug=servicio_slug,
            defaults={
                'nombre': servicio_nombre,
                'duracion_minutos': 30,
                'activo': True,
            },
        )
        if force:
            servicio.nombre = servicio_nombre
            servicio.duracion_minutos = 30
            servicio.activo = True
            servicio.save()

        self.stdout.write(self.style.SUCCESS('Seed demo listo.'))
