from django import template
register = template.Library()

from django.conf import settings

@register.inclusion_tag('clippy/clippy.html')
def clippy(element_id, size='14x110', bgcolor='#FFFFFF', wmode='opaque'):
    static_url = getattr(settings, 'STATIC_URL', 'MEDIA_URL') # backwards comaptibility with Django 1.2
    data = {
        'element_id':element_id,
        'STATIC_URL':static_url,
        'wmode': wmode,
        'bgcolor': bgcolor,
    }
    if size is not None:
        assert 'x' in size
        w, h = size.split('x')
        if w != '':
            data['width'] = w
        if h != '':
            data['height'] = h
            
    return data 

