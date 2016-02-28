from django.contrib import admin
from rental.models import Device, Event, Inventory, Manufacturer, Review, Rental
from django.db.models import Q
# Register your models here.

class AdminEvent(admin.ModelAdmin):
  filter_vertical = ("inventories",)
  event = None
  def formfield_for_manytomany(self, db_field, request, **kwargs):
    #SICK HAXORS 8-)
    if db_field.name == "inventories":
      event = Event.objects.filter(slug=request.path.split('/')[-2])
      kwargs["queryset"] = Inventory.objects.filter(Q(event=event) | Q(event=None))
    return super(AdminEvent, self).formfield_for_manytomany(db_field, request, **kwargs)
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

class RentalAdmin(admin.ModelAdmin):
  list_display = ('user', 'returned', 'device', 'device_id')
  list_filter = ('returned','user', 'inventory__device')
  def device(self,rental):
    return rental.inventory.device
  def device_id(self,rental):
    return rental.inventory.id


admin.site.register(Event,AdminEvent)
admin.site.register(Device, DeviceInline)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rental,RentalAdmin)
