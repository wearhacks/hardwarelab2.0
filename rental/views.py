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

##### 
# def home(request):
#    posts = json.loads(urlopen(config.A_BLOG_LINK + '/?json=1').read())["posts"]
#    events = Event.objects.all().filter(start_date__gt = datetime.datetime.now()).order_by('start_date')
#    if len(events) > 0:
#        event = events[0]
#    else:
#        event = None
#    content = {
#        'title' : "Home",
#        'config':config,
#        'blog_title' : posts[0]["title"],
#        'blog_excerpt' : posts[0]["excerpt"],
#        'blog_link' : posts[0]["url"],
#        'blog_image' : posts[0]["thumbnail_images"]["full"]["url"],
#        'event' : event,
#        'slides' : Slider.objects.filter(slider_location = 0).order_by('order'),
#        'past_events': Event.objects.all().filter(start_date__lt = datetime.datetime.now()).order_by('-start_date')[:3],
#    }
#
#
#    return render(request, 'index.html',content)