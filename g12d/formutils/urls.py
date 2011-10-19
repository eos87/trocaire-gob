from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('formutils.views',    
    url(r'^$', 'fill', name='fill'),
)