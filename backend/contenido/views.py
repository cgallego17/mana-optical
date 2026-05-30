from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Banner, HomeContent, Testimonio
from .serializers import BannerSerializer
from .serializers import HomeContentSerializer
from .serializers import TestimonioSerializer


class HomeContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        obj = HomeContent.objects.first()
        if not obj:
            obj = HomeContent.objects.create()
        return Response(HomeContentSerializer(obj).data)


class BannerListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Banner.objects.filter(activo=True).order_by('orden', 'id')
        return Response(BannerSerializer(qs, many=True).data)


class TestimonioListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Testimonio.objects.filter(activo=True).order_by('orden', 'id')
        return Response(TestimonioSerializer(qs, many=True).data)
