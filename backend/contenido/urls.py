from django.urls import path

from .views import BannerListView
from .views import HomeContentView
from .views import TestimonioListView

urlpatterns = [
    path('home/', HomeContentView.as_view(), name='contenido_home'),
    path('banners/', BannerListView.as_view(), name='contenido_banners'),
    path(
        'testimonios/',
        TestimonioListView.as_view(),
        name='contenido_testimonios',
    ),
]
