from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Categoria, Marca, Producto
from .serializers import (
    CategoriaSerializer,
    MarcaSerializer,
    ProductoAdminSerializer,
    ProductoDetailSerializer,
    ProductoListSerializer,
)


class ProductoPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ── Public ────────────────────────────────────────────────────────────────────

class MarcaListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = MarcaSerializer
    queryset = Marca.objects.filter(activa=True).order_by('nombre')


class CategoriaListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.filter(activa=True).order_by('nombre')


class ProductoListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductoListSerializer
    pagination_class = ProductoPagination

    def get_queryset(self):
        qs = Producto.objects.filter(activo=True).select_related('categoria', 'marca')

        categoria = self.request.query_params.get('categoria')
        marca = self.request.query_params.get('marca')
        q = self.request.query_params.get('q')

        if categoria:
            qs = qs.filter(categoria__slug=categoria)
        if marca:
            qs = qs.filter(marca__slug=marca)
        if q:
            qs = qs.filter(nombre__icontains=q)

        return qs.order_by('-creado_en')


class ProductoDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductoDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Producto.objects.filter(activo=True).select_related('categoria', 'marca')


# ── Admin ─────────────────────────────────────────────────────────────────────

class AdminMarcaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = MarcaSerializer
    queryset = Marca.objects.all().order_by('nombre')


class AdminMarcaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = MarcaSerializer
    queryset = Marca.objects.all()


class AdminCategoriaListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all().order_by('nombre')


class AdminCategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()


class AdminProductoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductoAdminSerializer
    pagination_class = ProductoPagination
    queryset = Producto.objects.all().select_related('categoria', 'marca').order_by('-creado_en')


class AdminProductoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductoAdminSerializer
    queryset = Producto.objects.select_related('categoria', 'marca').all()
