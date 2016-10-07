from django.contrib import admin
from rental.models import Device, Event, Inventory, Manufacturer, Review, Rental, UserProfile, Manager
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Q
# Register your models here.

class AdminEvent(admin.ModelAdmin):
  filter_vertical = ("inventories",)
  pass

class InventoryInline(admin.TabularInline):
  model = Inventory
  extra = 0

class DeviceInline(admin.ModelAdmin):
  model = Device
  inlines = [InventoryInline]

class InventoryAdmin(admin.ModelAdmin):
  list_display = ('device', 'serial_id')

class ManufacturerAdmin(admin.ModelAdmin):
  pass

class ReviewAdmin(admin.ModelAdmin):
  pass

class ReservationAdmin(admin.ModelAdmin):
  pass

class ManagerAdmin(admin.ModelAdmin):
  pass

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'users'

class RentalAdmin(admin.ModelAdmin):
  list_display = ('user', 'returned', 'device', 'device_id')
  list_filter = ('returned','user', 'inventory__device')
  def device(self,rental):
    return rental.inventory.device
  def device_id(self,rental):
    return rental.inventory.id

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Event,AdminEvent)
admin.site.register(Device, DeviceInline)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rental, RentalAdmin)
admin.site.register(Manager, ManagerAdmin)
