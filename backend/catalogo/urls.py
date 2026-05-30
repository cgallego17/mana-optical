from django.urls import path

from .views import ProductoDetailView, ProductoListView

urlpatterns = [
    path(
        'productos/',
        ProductoListView.as_view(),
        name='productos_list',
    ),
    path(
        'productos/<slug:slug>/',
        ProductoDetailView.as_view(),
        name='productos_detail',
    ),
]
