from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT, DEBUG

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'g12d.views.home', name='home'),    
    url(r'^xls/$', 'g12d.utils.save_as_xls', name='save_xls' ),
    url(r'^report/$', 'g12d.contraparte.views.generate_report', name='generate_report' ),    
    url(r'^ajax/proyectos/$', 'g12d.contraparte.views.get_proyectos', name='get_proyectos' ),
    url(r'^ajax/salidas/$', 'g12d.contraparte.views.get_salidas', name='get_salidas' ),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}),
    url(r'^fillout/', include('g12d.formutils.urls')),
    url(r'^proyecto/', include('g12d.contraparte.urls')),
    url(r'^programa/', include('g12d.trocaire.urls')),    
    
    url(r'^chaining/', include('smart_selects.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i/(?P<hash>\w+)$', 'g12d.contraparte.views.shortview', name='shortview'),
)

urlpatterns += patterns('g12d.contraparte.views',    
    url(r'^variables/$', 'variables', name='variables'),
    url(r'^variables/output/$', 'output', name='output'),    
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

if DEBUG:
    urlpatterns += patterns('',
                (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
                )
