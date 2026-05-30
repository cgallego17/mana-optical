from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from .models import CategoriaBlog, Post
from .serializers import CategoriaBlogSerializer
from .serializers import PostAdminSerializer
from .serializers import PostDetailSerializer
from .serializers import PostListSerializer


class CategoriaBlogListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CategoriaBlogSerializer

    def get_queryset(self):
        return CategoriaBlog.objects.filter(activa=True).order_by('nombre')


class PostListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostListSerializer

    def get_queryset(self):
        qs = Post.objects.filter(publicado=True).select_related('categoria')

        categoria = self.request.query_params.get('categoria')
        q = self.request.query_params.get('q')

        if categoria:
            qs = qs.filter(categoria__slug=categoria)
        if q:
            qs = qs.filter(titulo__icontains=q)

        return qs


class PostDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(publicado=True).select_related('categoria')


class AdminPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PostAdminSerializer

    def get_queryset(self):
        return Post.objects.all().select_related('categoria')


class AdminPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PostAdminSerializer

    def get_queryset(self):
        return Post.objects.all().select_related('categoria')
