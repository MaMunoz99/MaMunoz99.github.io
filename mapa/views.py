from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
import json
from .models import Camara, Camion, Deteccion

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

def api_estado_actual(request):
    # 1. Obtener la detección más reciente para cada PATENTE única (independientemente del ID de camión interno)
    # Esto soluciona el problema de ver la misma patente repetida si hay duplicados
    ids_ultimas = Deteccion.objects.values('id_camion__patente').annotate(max_id=Max('id')).values_list('max_id', flat=True)
    
    # 2. Obtener los detalles de esas detecciones únicas
    detecciones_actuales = Deteccion.objects.filter(id__in=ids_ultimas).select_related('id_camion', 'id_camara')

    # 3. Preparar el mapa de cámaras
    camaras = Camara.objects.all()
    mapa_camaras = {}
    for cam in camaras:
        mapa_camaras[cam.id] = {
            'id': cam.id,
            'latitud': float(cam.lat),
            'longitud': float(cam.long),
            'estado': cam.estado,
            'camiones': []
        }

    # 4. Asignar camiones a sus cámaras actuales (cada camión solo aparecerá en una cámara a la vez)
    for det in detecciones_actuales:
        if det.id_camara_id in mapa_camaras:
            mapa_camaras[det.id_camara_id]['camiones'].append({
                'patente': det.id_camion.patente,
                'fecha': det.fecha.strftime('%Y-%m-%d')
            })

    return JsonResponse(list(mapa_camaras.values()), safe=False)

def api_historial_camara(request, camara_id):
    # 1. Obtener la última vez que cada PATENTE única pasó por ESTA cámara específica
    ids_historial = Deteccion.objects.filter(id_camara_id=camara_id)\
                            .values('id_camion__patente')\
                            .annotate(max_id=Max('id'))\
                            .values_list('max_id', flat=True)
    
    # 2. Obtener los detalles de esas últimas pasadas por esta cámara
    detecciones = Deteccion.objects.filter(id__in=ids_historial)\
                            .select_related('id_camion')\
                            .order_by('-fecha', '-id')[:50]
    
    historial = []
    for det in detecciones:
        historial.append({
            'patente': det.id_camion.patente,
            'fecha': det.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'id_frame': det.id_camion.id_frame
        })

    return JsonResponse(historial, safe=False)

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
