from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('g12d.contraparte.views',    
    url(r'^$', 'filtro_proyecto', name='filtro_proyecto'),
)