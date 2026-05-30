from django.urls import path

from .views import (
    AdminPostDetailView,
    AdminPostListCreateView,
    CategoriaBlogListView,
    PostDetailView,
    PostListView,
)

urlpatterns = [
    path(
        'categorias/',
        CategoriaBlogListView.as_view(),
        name='blog_categorias',
    ),
    path('posts/', PostListView.as_view(), name='blog_posts_list'),
    path(
        'posts/<slug:slug>/',
        PostDetailView.as_view(),
        name='blog_posts_detail',
    ),

    path(
        'admin/posts/',
        AdminPostListCreateView.as_view(),
        name='admin_blog_posts_list_create',
    ),
    path(
        'admin/posts/<int:pk>/',
        AdminPostDetailView.as_view(),
        name='admin_blog_posts_detail',
    ),
]
