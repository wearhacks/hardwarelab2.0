from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
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



class UserInfo(models.Model):
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  first_name = models.CharField(max_length = 50)
  last_name = models.CharField(max_length = 50)
  phone_regex = RegexValidator(regex = r'^\+?1?\d{9,15}$',
                              message = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
  phone_number = models.CharField(validators = [phone_regex], blank=True, max_length = 15) #validators should be a list

class Device(models.Model):
  name = models.CharField(max_length = 50)
  company = models.CharField(max_length = 50)
  small_desc = models.CharField(max_length = 250)
  image = models.ImageField(upload_to = get_image_filename, blank = True, null = True)

  def __unicode__(self):
    return u"%s" % self.name

class Inventory(models.Model):
  device = models.ForeignKey(Device)
  serial_id = models.CharField(max_length = 50)
  def __unicode__(self):
    return u"%s [ID: %s]" % (self.device.name,self.serial_id)
  class Meta:
        verbose_name_plural = "Inventories"
class Rental(models.Model):
  user = models.ForeignKey(User)
  device = models.ForeignKey(Device)
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)


  def __unicode__(self):
    return u"%s" % self.id

class Event(models.Model):
  name = models.CharField(max_length = 50)
  device = models.ManyToManyField(Inventory)
  def __unicode__(self):
    return u"%s" % self.name
