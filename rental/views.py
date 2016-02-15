from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from models import Device, Event
# Create your views here.
def devices(request, event_name):
  print event_name
  event = Event.objects.get(name=event_name)
  devices = event.devices.all()
  content = {
    'event' : event,
    'devices' : devices
  }
  return render(request,'devices.html', content)

def view_device(request, event_name, device_name):
  device = Device.objects.get(name=device_name)
  event = Event.objects.get(name=event_name)

  content = {
    'event' : event,
    'device' : device
  }
  return render(request,'view_device.html', content)

def home(request):
  content = {
    'events' : Event.objects.all()
  }
  return render(request,'events.html', content)

