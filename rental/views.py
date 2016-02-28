from django.shortcuts import render
from django.template.defaulttags import register
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from .models import UserProfile, Device, Event, Inventory
from .forms import UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
# Create your views here.

@register.filter(name='lookup')
def cut(value, arg):
    return value[arg]


def devices(request, event_slug):
  event = Event.objects.get(slug=event_slug)
  devices = Device.objects.all()
  event_inventory = Inventory.objects.filter(event=event)
  inventories = {}
  for device in devices:
      #taking all the stock
      inventories[device.name] = event_inventory.filter(device=device)

  content = {
    'event' : event,
    'devices' : devices,
    'inventories' : inventories
  }
  return render(request,'devices.html', content)

def view_device(request, event_slug, device_name):
  device = Device.objects.get(name=device_name)
  event = Event.objects.get(slug=event_slug)

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

@login_required
def user_profile(request, user_name):
  user = User.objects.get(username=user_name)
  user_form = UserProfileForm(instance=user)

  ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('phone_number',))
  formset = ProfileInlineFormset(instance=user)

  if request.user.is_authenticated(): #and request.user.id == user.id:
    if request.method == "POST":
      user_form = UserProfileForm(request.POST, request.FILES, instance=user)
      formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

      if user_form.is_valid():
        created_user = user_form.save(commit=False)
        formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

        if formset.is_valid():
          created_user.save()
          formset.save()
          return HttpResponseRedirect('/', user_name)

    return render(request, "user_profile.html", {
    "noodle": user_name,
    "noodle_form": user_form,
    "formset": formset,
    })
  else:
    raise PermissionDenied
