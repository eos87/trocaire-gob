from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('g12d.formutils.views',    
    url(r'^$', 'fill', name='fill'),
)