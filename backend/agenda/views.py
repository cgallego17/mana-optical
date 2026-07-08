from datetime import date, datetime, time, timedelta

from django.utils.timezone import localdate
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DiaExcepcion, HorarioAtencion, Reserva, Servicio
from .serializers import (
    DiaExcepcionSerializer,
    HorarioAtencionSerializer,
    ReservaAdminSerializer,
    ReservaCreateSerializer,
    ServicioAdminSerializer,
    ServicioSerializer,
)


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

        servicio = None
        servicio_id = request.query_params.get('servicio')
        if servicio_id:
            try:
                servicio = Servicio.objects.get(pk=servicio_id)
            except (Servicio.DoesNotExist, ValueError):
                return Response({'detail': 'Servicio no existe.'}, status=400)

        if servicio and servicio.hora_inicio and servicio.hora_fin:
            # El servicio tiene horario propio: es independiente del horario
            # semanal y de las excepciones de fecha del negocio.
            if servicio.dias_disponibles and fecha.weekday() not in servicio.dias_disponibles:
                return Response({'fecha': fecha_str, 'slots': []})
            hora_inicio, hora_fin = servicio.hora_inicio, servicio.hora_fin
        else:
            abierto, hora_inicio, hora_fin = HorarioAtencion.resolver_fecha(fecha)
            if not abierto:
                return Response({'fecha': fecha_str, 'slots': []})
            if servicio and servicio.dias_disponibles and fecha.weekday() not in servicio.dias_disponibles:
                return Response({'fecha': fecha_str, 'slots': []})

        slots = build_slots(hora_inicio, hora_fin, 30)

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


class ExcepcionListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DiaExcepcionSerializer

    def get_queryset(self):
        return DiaExcepcion.objects.filter(fecha__gte=localdate())


class AdminExcepcionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DiaExcepcionSerializer
    queryset = DiaExcepcion.objects.all()


class AdminExcepcionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = DiaExcepcionSerializer
    queryset = DiaExcepcion.objects.all()


class AdminReservaListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ReservaAdminSerializer

    def get_queryset(self):
        return Reserva.objects.all().select_related('servicio', 'cliente').order_by('-fecha', '-hora')


class AdminReservaDetailView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ReservaAdminSerializer
    queryset = Reserva.objects.all()


class AdminServicioListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ServicioAdminSerializer
    queryset = Servicio.objects.all().order_by('nombre')


class AdminServicioDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ServicioAdminSerializer
    queryset = Servicio.objects.all()


class HorarioListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HorarioAtencionSerializer

    def get_queryset(self):
        HorarioAtencion.ensure_semana()
        return HorarioAtencion.objects.all()


class AdminHorarioListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = HorarioAtencionSerializer

    def get_queryset(self):
        HorarioAtencion.ensure_semana()
        return HorarioAtencion.objects.all()


class AdminHorarioDetailView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = HorarioAtencionSerializer
    queryset = HorarioAtencion.objects.all()
