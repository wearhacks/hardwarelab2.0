from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from models import Device
# Create your views here.
def devices(request):
  if request.method == 'GET':
    json_devices = serializers.serialize("json", Device.objects.all())
    return HttpResponse(json_devices, content_type='application/json')
