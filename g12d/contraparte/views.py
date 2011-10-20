# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from g12d.forms import *
from models import *

def filtro_proyecto(request):
    proy_params = {}
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proy_params['organizacion'] = form.cleaned_data['organizacion']
            proy_params['proyecto'] = form.cleaned_data['proyecto']
            proy_params['mes__in'] = form.cleaned_data['meses']
            proy_params['fecha__year'] = form.cleaned_data['anio']
            
            proy_params = checkParams(proy_params)
            request.session['proy_params'] = proy_params 
            
            query = _get_query(request)
    else:
        form = ProyectoForm()
            
    return render_to_response('contraparte/filtro.html', RequestContext(request, locals()))

def _get_query(request):
    return Actividad.objects.filter(**request.session['proy_params'])

#verificcar que no existan parametros vacios
checkParams = lambda x: dict((k, v) for k,v in x.items() if x[k])