from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.forms import ModelForm
import datetime
import os


def get_image_filename(instance, old_filename):
  folder = ''
  if hasattr(instance, 'MEDIA_URL'):
    folder = instance.MEDIA_URL

  filename = os.path.join(
    os.path.dirname(old_filename),
    folder,
    old_filename
  )
  return filename

def check_user_info(sender, request, user, **kwargs):
  user_profile = UserProfile(user = user)
  response = login(request, *args, **kwargs)
  if request.user.is_authenticated():
    messages.info(request, "Welcome auth...")
    if user_profile.phone_number is None:
      messages.info(request, "Welcome phone...")
  return response



class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  phone_regex = RegexValidator(regex = r'^\+?1?\d{9,15}$',
                              message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  phone_number = models.CharField(validators = [phone_regex], blank=True, max_length = 15) #validators should be a list

  def __unicode__(self):
    return u"%s" % self.user

class Manager(models.Model):
  user = models.ForeignKey(User)
  def __unicode__(self):
    return u"%s" % self.user
  

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class Manufacturer(models.Model):
  name = models.CharField(max_length = 50)
  region = models.CharField(max_length = 50)
  contact_name = models.CharField(max_length = 50)
  contact_email = models.EmailField(max_length = 254)
  def __unicode__(self):
    return u"%s" % self.name

class Device(models.Model):
  name = models.CharField(max_length = 100)
  manufacturer = models.ForeignKey(Manufacturer, default = 0)
  description = models.CharField(max_length = 250)
  image = models.ImageField(upload_to = get_image_filename, blank = True, null = True)

  def __unicode__(self):
    return u"%s" % self.name

class Inventory(models.Model):
  device = models.ForeignKey(Device)
  serial_id = models.CharField(max_length = 50) #manually defined with the format: manufacturer.id+device.id+(prev_inventory.id + 1)
  rented = models.BooleanField(default = False)

  def __unicode__(self):
    return u"%s [ID: %s]" % (self.device.name,self.serial_id)
  class Meta:
    verbose_name_plural = "Inventory"
    order_with_respect_to = 'device'

class Event(models.Model):
  name = models.CharField(max_length = 50)
  slug = models.SlugField(blank=True,
         help_text="ie: Short name, required field for event page: http://wearhacks.com/events/<slug>")
  start_date = models.DateTimeField(null = True)
  end_date = models.DateTimeField(null = True)
  host = models.CharField(max_length = 100, null = True)
  managers = models.ManyToManyField(Manager)
  devices = models.ManyToManyField(Device)
  inventories = models.ManyToManyField(Inventory, blank = True)

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify('%s-%d' % (self.name, self.start_date.year))
    super(Event, self).save(*args, **kwargs)

  def __unicode__(self):
    return u"%s" % self.name

class Rental(models.Model):
  user = models.ForeignKey(User)
  inventory = models.ForeignKey(Inventory, null=True, blank = True)
  device = models.ForeignKey(Device)
  event = models.ForeignKey(Event)
  reservation = models.BooleanField(default = True) 
  created_at = models.DateTimeField(auto_now_add = True)

  hack_finished = models.BooleanField(default = False)
  returned = models.BooleanField(default = False)
  
  returned_at = models.DateTimeField(null = True, blank=True)

  def __unicode__(self):
    if self.inventory:
      return u"%s %s" % (self.user, self.inventory.serial_id)
    if not self.inventory:
      return u"%s %s" % (self.user, self.device)

class Review(models.Model):
  user = models.ForeignKey(UserProfile)
  devices = models.ManyToManyField(Device)
  comfort_level = models.IntegerField()
  device_rating = models.IntegerField()
  improvements = models.CharField(max_length = 500)
  other_comments = models.CharField(max_length = 500)