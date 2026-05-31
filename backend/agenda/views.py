from datetime import date, datetime, time, timedelta

from django.utils.timezone import localdate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Reserva, Servicio
from .serializers import ReservaAdminSerializer, ReservaCreateSerializer, ServicioSerializer


def build_slots(start: time, end: time, step_minutes: int):
    slots = []
    dt = datetime.combine(date.today(), start)
    dt_end = datetime.combine(date.today(), end)
    step = timedelta(minutes=step_minutes)
    while dt <= dt_end:
        slots.append(dt.time().replace(second=0, microsecond=0))
        dt += step
    return slots


class DisponibilidadView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        fecha_str = request.query_params.get('fecha')
        if not fecha_str:
            return Response(
                {
                    'detail': (
                        'Parametro "fecha" es requerido '
                        '(YYYY-'
                        'MM-'
                        'DD).'
                    ),
                },
                status=400,
            )

        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            return Response({'detail': 'Formato de fecha inválido.'}, status=400)

        if fecha < localdate():
            return Response({'fecha': fecha_str, 'slots': []})
        if fecha.weekday() == 6:
            return Response({'fecha': fecha_str, 'slots': []})

        # Horario base: 9:00 a 21:00 cada 30 min
        slots = build_slots(time(9, 0), time(21, 0), 30)

        reserved = set(
            Reserva.objects.filter(fecha=fecha)
            .exclude(estado=Reserva.Estado.CANCELADA)
            .values_list('hora', flat=True)
        )

        return Response(
            {
                'fecha': fecha_str,
                'slots': [
                    {
                        'hora': s.strftime('%H:%M'),
                        'disponible': s not in reserved,
                    }
                    for s in slots
                ],
            },
        )


class ReservaCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ReservaCreateSerializer


class ServicioListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServicioSerializer

    def get_queryset(self):
        return Servicio.objects.filter(activo=True).order_by('nombre')


class AdminReservaListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ReservaAdminSerializer

    def get_queryset(self):
        return Reserva.objects.all().select_related('servicio', 'cliente').order_by('-fecha', '-hora')
