from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Cliente
from .serializers import ClienteSerializer


class ClienteListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClienteSerializer

    def get_queryset(self):
        return Cliente.objects.all().order_by('-creado_en')


class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = ClienteSerializer

    def get_queryset(self):
        return Cliente.objects.all()
