from pathlib import Path

from django.contrib import admin
from django.http import FileResponse, HttpResponse
from django.urls import include, path, re_path
from django.views.static import serve

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Carpeta con el build de Vue
DIST = Path(__file__).resolve().parent.parent.parent / 'web' / 'dist'


def vue_app(request, **_kwargs):
    """Sirve index.html para cualquier ruta no-API (SPA fallback)."""
    index = DIST / 'index.html'
    if index.exists():
        return FileResponse(open(index, 'rb'), content_type='text/html; charset=utf-8')
    return HttpResponse(
        '<h1>Frontend no compilado</h1>'
        '<p>Ejecuta <code>npm run build</code> dentro de la carpeta <code>web/</code>.</p>',
        status=503,
        content_type='text/html',
    )


urlpatterns = [
    path('django-admin/', admin.site.urls),

    # API REST
    path('api/', include('api.urls')),
    path('api/auth/token/',   TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(),    name='token_refresh'),

    # Archivos estáticos del build de Vue
    re_path(r'^assets/(?P<path>.+)$', serve, {'document_root': str(DIST / 'assets')}),
    re_path(
        r'^(?P<path>favicon\.svg|logo\.png|logo-amarillo\.png|icons\.svg'
        r'|sw\.js|manifest\.webmanifest|robots\.txt|sitemap\.xml)$',
        serve, {'document_root': str(DIST)},
    ),

    # SPA catch-all — debe ir al final
    re_path(r'^.*$', vue_app),
]
