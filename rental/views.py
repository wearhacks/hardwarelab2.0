from django.shortcuts import render
from django.template.defaulttags import register
from django.http import HttpResponse,JsonResponse, HttpResponseBadRequest
from django.core import serializers
from models import Device, Event, Inventory, Rental
from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q
import json
# Create your views here.

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]


def devices(request, event_slug):
  event = Event.objects.get(slug=event_slug)
  devices = Device.objects.all()
  event_inventory = Inventory.objects.filter(event=event)
  inventories = {}
  inventories_free = {}
  for device in devices:
      #taking all the stock
      free_inventory = Inventory.objects.filter(
        Q(event=event,device=device,rental=None) 
        | Q(event=event,device=device,rental__returned=True))
      inventories[device.name] = event_inventory.filter(device=device)
      inventories_free[device.name] = free_inventory.count()
  content = {
    'event' : event,
    'devices' : devices,
    'inventories' : inventories,
    'inventories_free' : inventories_free
  }
  return render(request,'devices.html', content)

def view_device(request, event_slug, device_name):
  device = Device.objects.get(name=device_name)
  event = Event.objects.get(slug=event_slug)
  event_inventory = Inventory.objects.filter(event=event, device=device)
  rentals = Rental.objects.filter(inventory = event_inventory, returned = False)
  
  free = event_inventory.count() - rentals.count()
  content = {
    'event' : event,
    'device' : device,
    'rentals' : rentals,
    'free' : free
  }
  return render(request,'view_device.html', content)

def home(request):
  content = {
    'events' : Event.objects.all()
  }
  return render(request,'events.html', content)

#custom view to see where all the hardware are located
def hardware_location(request):
    inventories = {}
    free_inventories = {}
    for event in Event.objects.all():
        event_inventory = Inventory.objects.filter(event=event)
        inventories[event.name] = {}
        for device in Device.objects.all():
            inventories[event.name][device.name] = event_inventory.filter(device=device)

    unassigned_inventory = Inventory.objects.filter(event=None)
    for device in Device.objects.all():
        free_inventories[device.name] = unassigned_inventory.filter(device=device)

    return render(request,'hardware_location.html', {'inventories': inventories, 'free_inventories': free_inventories})


def rent_device(request):
  user = User.objects.get(username=request.GET['user'])

  event = Event.objects.get(name=request.GET['event'])
  device = Device.objects.get(name=request.GET['device'])
  device_rentals = Rental.objects.filter(inventory__device=device, returned = False)
  free_inventory = Inventory.objects.filter(Q(event=event,device=device) & ~Q(rental=device_rentals)) 
  response = {}
  response['username'] = user.username
  if user.socialaccount_set.count() > 0:
    response['avatar'] = user.socialaccount_set.all()[0].get_avatar_url()
  
  if free_inventory.count() > 0:
    new_rental = Rental(user = user, inventory = free_inventory[0])
    new_rental.save()
    rentals = Rental.objects.filter(inventory__event = event, inventory__device = device, returned = False)
    free = free_inventory.count()
    return render(request, 'partials/device_rentals.html',   {'rentals':rentals, 'free': free})
  else:
    return HttpResponseBadRequest("Sorry, there are no more " + device.name + " in stock!")
  


def user_settings(request, user_name):
  user = User.objects.get(username = user_name)

  content = {
    'user' : user
  }

  return render(request,'user_profile.html', content)
