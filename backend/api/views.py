from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from agenda.models import Servicio
from catalogo.models import Producto


@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({'status': 'ok'})


@api_view(['GET'])
@permission_classes([AllowAny])
def busqueda(request):
    q = (request.query_params.get('q') or '').strip()
    if not q:
        return Response({'q': q, 'results': []})

    limit = 8
    results: list[dict[str, str]] = []

    productos = (
        Producto.objects.filter(activo=True, nombre__icontains=q)
        .only('nombre', 'slug')
        .order_by('nombre')[:limit]
    )
    for p in productos:
        results.append(
            {
                'title': p.nombre,
                'subtitle': 'Producto',
                'href': f'/producto/{p.slug}',
            }
        )

    if len(results) < limit:
        servicios = (
            Servicio.objects.filter(activo=True, nombre__icontains=q)
            .only('nombre')
            .order_by('nombre')[: (limit - len(results))]
        )
        for s in servicios:
            results.append(
                {
                    'title': s.nombre,
                    'subtitle': 'Servicio',
                    'href': '/servicios',
                }
            )

    if len(results) < limit:
        sugerencias = [
            {
                'title': 'Agenda una cita',
                'subtitle': 'Agenda',
                'href': '/agenda',
            },
            {
                'title': 'Contáctanos',
                'subtitle': 'Soporte',
                'href': '/contacto',
            },
        ]
        t = q.lower()
        for item in sugerencias:
            if len(results) >= limit:
                break
            if t in item['title'].lower() or t in item['subtitle'].lower():
                results.append(item)

    return Response({'q': q, 'results': results[:limit]})
