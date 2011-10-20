from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('contraparte.views',    
    url(r'^$', 'filtro_proyecto', name='filtro_proyecto'),
    url(r'^resultado/(?P<id>\d+)/$', 'resultado_detail', name='resultado_detail'),
    url(r'^resultado/(?P<id>\d+)/output/$', 'output', name='output'),
)