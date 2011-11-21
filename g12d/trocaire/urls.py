from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('g12d.trocaire.views',    
    url(r'^$', 'filtro_programa', name='filtro_programa'),    
)