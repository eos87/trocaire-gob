# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from contraparte.models import *
from django.utils import simplejson

#ugly code but functional

to_choices = lambda x: [(y,unslugify(y)) for y in x]

def unslugify(value):
    return ' '.join([s.capitalize() \
                     if i == 0 else s \
                     for i, s in enumerate(value.split('_'))])
    
def save_as_xls(request):
    tabla = request.POST['tabla']    
    response = render_to_response('xls.html', {'tabla': tabla, })
    response['Content-Disposition'] = 'attachment; filename=tabla.xls'
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Charset'] ='UTF-8'
    return response

def test(request):        
    response = render_to_response('test.html', {})
    response['Content-Disposition'] = 'attachment; filename=imagen.doc'
    response['content-transfer-encoding'] = 'base64'
    response['Content-Type'] = 'application/msword'
    response['Charset'] ='UTF-8'
    return response

def get_proyectos(request):
    ids = request.GET.get('ids', '')
    if ids:
        try:
            ids = ids.split(',')
            proyectos = Proyecto.objects.filter(organizacion__id__in=map(int, ids)).values('id', 
                                                                                           'organizacion__nombre_corto', 
                                                                                           'codigo')
            print proyectos
        except:
            return HttpResponse(':(')
    else:
        return HttpResponse(':(')
    return HttpResponse(simplejson.dumps(list(proyectos)), mimetype="application/json")