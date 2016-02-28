from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Examples:
    url(r'^$', 'rental.views.home', name='home'),
    url(r'^hardwarelab/(?P<event_slug>.*)/$', 'rental.views.devices', name='devices'),
    url(r'^hardwarelab/(?P<event_slug>.*)/(?P<device_name>.*)','rental.views.view_device'),
    url(r'^hardwarelab/inventory','rental.views.hardware_location'),
    url(r'^user/(?P<user_name>.*)','rental.views.user_settings'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/allinventory', 'rental.views.hardware_location'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api/rent/$', 'rental.views.rent_device'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
