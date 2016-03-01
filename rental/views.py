from django.shortcuts import render
from django.template.defaulttags import register
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.core import serializers
from models import UserProfile, Device, Event, Inventory, Rental
from forms import UserProfileForm
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import json
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

def user_orders(request):
  user = User.objects.get(pk = request.user.id)
  rentals = Rental.objects.filter(user = user)

  return render(request, 'user_orders.html', {'rentals': rentals})

def cancel_reservation(request):
  rental = Rental.objects.get(pk = request.GET['rental_id'])
  try:
    rental.delete()
  except Exception as e:
    return HttpResponseBadRequest('An error occured: %s', e)
  else:
    return HttpResponse('Reservation Canceled')