from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Camara

def mapa_view(request):
    return render(request, 'mapa/mapa.html')

def api_pines(request):
    # Obtenemos las cámaras y las formateamos para que el JS las entienda como pines
    camaras = Camara.objects.all().values('id', 'lat', 'long', 'estado')
    pines = []
    for c in camaras:
        pines.append({
            'id': c['id'],
            'nombre': f"Cámara {c['id']}",
            'latitud': float(c['lat']),
            'longitud': float(c['long']),
            'descripcion': f"Estado: {'Activa' if c['estado'] else 'Inactiva'}"
        })
    return JsonResponse(pines, safe=False)

@csrf_exempt
def api_crear_pin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nueva_camara = Camara.objects.create(
                lat=data.get('latitud'),
                long=data.get('longitud'),
                estado=True
            )
            return JsonResponse({'status': 'success', 'pin_id': nueva_camara.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
