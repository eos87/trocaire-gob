from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT, DEBUG

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'g12d.views.home', name='home'),
    url(r'^xls/$', 'g12d.utils.save_as_xls', name='save_xls' ),
    url(r'^fillout/$', include('formutils.urls')),
    url(r'^proyecto/', include('contraparte.urls')),    
    
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

if DEBUG:
    urlpatterns += patterns('',
                (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
                )
