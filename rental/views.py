import json
from datetime import datetime
from django.shortcuts import render
from django.template.defaulttags import register
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core import serializers
from models import UserProfile, Device, Event, Inventory, Rental, Manager
from forms import UserProfileForm
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q
# Create your views here.

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]

def phone_number_warning_message(**kwargs):
    """
    Add a welcome message when the user logs in
    """
    user_profile = UserProfile.objects.get(user = kwargs["user"])
    if user_profile.phone_number in ['', None]:
      messages.warning(kwargs["request"], "You must add your phone number to your profile")

user_logged_in.connect(phone_number_warning_message)

def devices(request, event_slug):
  event = Event.objects.get(slug=event_slug)
  devices = event.devices.all()
  inventories = {}
  inventories_free = {}
  for device in devices:
      #taking all the stock
      event_inventory = Inventory.objects.filter(event=event, device=device)
      rentals = Rental.objects.filter(event = event, device = device, returned = False)
      inventories_free[device.name] = event_inventory.count() - rentals.count()
      inventories[device.name] = event_inventory.filter(device=device)

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
  rentals = Rental.objects.filter(event = event, device = device, returned = False)
  
  free = event_inventory.count() - rentals.count()

  user_profile = ''

  if request.user.is_authenticated():
    phone_number_warning_message(request = request, user = request.user)
    user_profile = UserProfile.objects.get(user = request.user)
  content = {
    'event' : event,
    'device' : device,
    'rentals' : rentals,
    'free' : free,
    'user_profile' : user_profile
  }
  return render(request,'view_device.html', content)

def home(request):
  events = Event.objects.all()
  managed_events = []
  user = ''
  if request.user.is_authenticated():
    user = request.user
    for event in events:
      managers = event.managers.all()
      manager = True
      try:
        event.managers.get(user = user)
      except Manager.DoesNotExist:
        manager = False

      if manager:
        managed_events.append(event)

  content = {
    'events' : events,
    'managed_events' : managed_events,
    'u' : user
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

def reserve_device(request):
  #--------variables from the request
  user = User.objects.get(username=request.GET['user'])
  event = Event.objects.get(name=request.GET['event'])
  device = Device.objects.get(name=request.GET['device'])

  #--------number of devices that have been reserved/rented
  rentals = Rental.objects.filter(event = event, device = device, returned = False)

  free_inventory = Inventory.objects.filter(event=event, device=device).count() - rentals.count()

  
  if free_inventory > 0:
    new_rental = Rental(user = user, event = event, device = device)
    new_rental.save()
    r = Rental.objects.filter(event = event, device = device, returned = False) #grab the current rentals again after saving the current reservation
    free = free_inventory - 1  #decrease the free count since a new rental is made

    return JsonResponse(
      {'rental_render': render(request, 'partials/device_rentals.html',{'rentals': r, 'free': free }).content,
       'free_inventory' : free
      })

  else:
    return HttpResponseBadRequest("Sorry, there are no more " + device.name + " in stock!")

def cancel_reservation(request):
  rental = Rental.objects.get(pk = request.GET['rental_id'])
  rental.delete()
  
  return HttpResponse('Reservation Canceled')

def rent_device(request):
  rental = Rental.objects.get(pk = request.GET['rental_id'])
  inventory = Inventory.objects.get(pk = request.GET['inventory_id'])
  
  inventory.rented = True
  rental.reservation = False
  rental.inventory = inventory
  rental.device = inventory.device
  
  rental.save()
  inventory.save()
  

  reservations = Rental.objects.filter(event = rental.event, reservation = True)
  rentals = Rental.objects.filter(event = rental.event, reservation = False, returned = False)

  free_inventory = {}
  for device in rental.event.devices.all():
   free_inventory[device.name] = Inventory.objects.filter(event=rental.event, device=device, rented = False)

  context = {
   'reservations' : reservations,
   'rentals' : rentals,
   'free_inventories': free_inventory,
  }
  return render(request, 'partials/manager_partial.html', context)

def return_device(request):
  rental = Rental.objects.get(pk = request.GET['rental_id'])
  inventory = Inventory.objects.get(pk = rental.inventory.id)
  
  rental.returned = True
  inventory.rented = False
  rental.hack_finished = False
  if request.GET['hack_finished'] == 'on':
    rental.hack_finished = True
  rental.returned_at = datetime.now()
  
  rental.save()
  inventory.save()

  #-----------intentionally left here
  # reservations = Rental.objects.filter(event = rental.event, reservation = True)
  # rentals = Rental.objects.filter(event = rental.event, reservation = False, returned = False)

  # free_inventory = {}
  # for device in rental.event.devices.all():
  #   free_inventory[device.name] = Inventory.objects.filter(event=rental.event, device=device, rented = False)

  # context = {
  #   'reservations' : reservations,
  #   'rentals' : rentals,
  #   'free_inventories': free_inventory,
  # }
  # return render(request, 'partials/manager_partial.html', context)
  return HttpResponse('Returned!')
      

@login_required
def user_profile(request):
  user = User.objects.get(pk=request.user.id)
  user_profile_form = UserProfileForm(instance=user)

  ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('phone_number',))
  UserProfileFormset = ProfileInlineFormset(instance=user)

  if request.user.is_authenticated(): #and request.user.id == user.id:
    if request.method == "POST":
      user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
      UserProfileFormset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

      if user_profile_form.is_valid():
        created_user = user_profile_form.save(commit=False)
        UserProfileFormset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

        if UserProfileFormset.is_valid():
          created_user.save()
          UserProfileFormset.save()
          return HttpResponseRedirect('/', user.username)

    context = {
      "user_name": user.username,
      "user_profile_form": user_profile_form,
      "user_profile_formset": UserProfileFormset,
    }
    return render(request, "user_profile.html", context)
  else:
    raise PermissionDenied

@login_required
def user_orders(request):
  user = User.objects.get(pk = request.user.id)
  rentals = Rental.objects.filter(user = user, returned = False)

  return render(request, 'user_orders.html', {'rentals': rentals})


@login_required
def event_manager(request, event_slug):
  event = Event.objects.get(slug = event_slug)

  managers = event.managers.all()
  manager = True
  try:
    event.managers.get(user = request.user)
  except Manager.DoesNotExist:
    manager = False

  if manager:
    devices = event.devices.all()
    event_inventory = event.inventories.all()
    free_inventory = {}
    for device in devices:
      free_inventory[device.name] = Inventory.objects.filter(event=event, device=device, rented = False)

    reservations = Rental.objects.filter(event = event, reservation = True)
    rentals = Rental.objects.filter(event = event, reservation = False, returned = False)

    context = {
      'reservations' : reservations,
      'rentals' : rentals,
      'free_inventories': free_inventory
    }
    return render(request, 'event_manager.html', context)
  else:
    # messages.info(request, "You are not a manager")
    return HttpResponseBadRequest('You no manager!')

