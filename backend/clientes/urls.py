from django.urls import path

from .views import ClienteDetailView, ClienteListCreateView

urlpatterns = [
    path('', ClienteListCreateView.as_view(), name='clientes_list_create'),
    path('<int:pk>/', ClienteDetailView.as_view(), name='clientes_detail'),
]
