from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Pin

def mapa_view(request):
    return render(request, 'mapa/mapa.html')

def api_pines(request):
    pines = Pin.objects.all().values('id', 'nombre', 'latitud', 'longitud', 'descripcion')
    return JsonResponse(list(pines), safe=False)

@csrf_exempt
def api_crear_pin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nuevo_pin = Pin.objects.create(
                nombre=data.get('nombre', 'Nuevo Pin'),
                latitud=data.get('latitud'),
                longitud=data.get('longitud'),
                descripcion=data.get('descripcion', '')
            )
            return JsonResponse({'status': 'success', 'pin_id': nuevo_pin.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
