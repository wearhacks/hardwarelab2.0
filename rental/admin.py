from django.contrib import admin
from rental.models import Device, Event, Inventory, Manufacturer, Review

# Register your models here.

class AdminEvent(admin.ModelAdmin):
  filter_vertical = ("inventories",)

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
 
admin.site.register(Event,AdminEvent)
admin.site.register(Device, DeviceInline)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Review, ReviewAdmin)

