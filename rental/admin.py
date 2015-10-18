from django.contrib import admin
from rental.models import Device,Event,Inventory

# Register your models here.

class AdminEvent(admin.ModelAdmin):
  filter_vertical = ("device",)

class InventoryInline(admin.TabularInline):
  model = Inventory
  extra = 0
class DeviceInline(admin.ModelAdmin):
  model = Device
  inlines = [InventoryInline]

class InventoryAdmin(admin.ModelAdmin):
  list_display = ('device', 'serial_id')

admin.site.register(Event,AdminEvent)
admin.site.register(Device, DeviceInline)
admin.site.register(Inventory, InventoryAdmin)

