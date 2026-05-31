from django.urls import path

from .views import (
    AdminCategoriaDetailView,
    AdminCategoriaListCreateView,
    AdminMarcaDetailView,
    AdminMarcaListCreateView,
    AdminProductoDetailView,
    AdminProductoListCreateView,
    CategoriaListView,
    MarcaListView,
    ProductoDetailView,
    ProductoListView,
)

urlpatterns = [
    path('productos/', ProductoListView.as_view(), name='productos_list'),
    path('productos/<slug:slug>/', ProductoDetailView.as_view(), name='productos_detail'),
    path('marcas/', MarcaListView.as_view(), name='marcas_list'),
    path('categorias/', CategoriaListView.as_view(), name='categorias_list'),

    path('admin/marcas/', AdminMarcaListCreateView.as_view(), name='admin_marcas_list_create'),
    path('admin/marcas/<int:pk>/', AdminMarcaDetailView.as_view(), name='admin_marcas_detail'),
    path('admin/categorias/', AdminCategoriaListCreateView.as_view(), name='admin_categorias_list_create'),
    path('admin/categorias/<int:pk>/', AdminCategoriaDetailView.as_view(), name='admin_categorias_detail'),
    path('admin/productos/', AdminProductoListCreateView.as_view(), name='admin_productos_list_create'),
    path('admin/productos/<int:pk>/', AdminProductoDetailView.as_view(), name='admin_productos_detail'),
]
