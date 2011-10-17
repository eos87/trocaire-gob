# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from g12d.forms import *

def filtro_proyecto(request):
    form = ProyectoForm()
    return render_to_response('contraparte/filtro.html', RequestContext(request, locals()))