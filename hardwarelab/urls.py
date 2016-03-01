from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    url(r'^$', 'rental.views.home', name='home'),
    
    url(r'^hardwarelab/inventory','rental.views.hardware_location'),
    url(r'^hardwarelab/(?P<event_slug>.*)/$', 'rental.views.devices', name='devices'),
    url(r'^hardwarelab/(?P<event_slug>.*)/manager', 'rental.views.event_manager'),
    url(r'^hardwarelab/(?P<event_slug>.*)/(?P<device_name>.*)','rental.views.view_device'),
    
    url(r'^me/','rental.views.user_profile'),
    url(r'^hardwarelab/me/orders','rental.views.user_orders'),

    url(r'^api/reserve/$', 'rental.views.reserve_device'),
    url(r'^api/rent/$', 'rental.views.rent_device'),
    url(r'^api/cancel-reservation/$', 'rental.views.cancel_reservation'),

    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/allinventory', 'rental.views.hardware_location'),
    url(r'^accounts/', include('allauth.urls')),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
