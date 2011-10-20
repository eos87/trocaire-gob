# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.db.models.loading import get_model
from django.http import HttpResponseRedirect
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
            
            resultados = Resultado.objects.filter(proyecto=proy_params['proyecto'])            
    else:
        form = ProyectoForm()
            
    return render_to_response('contraparte/filtro.html', RequestContext(request, locals()))

def _get_query(request):
    return Actividad.objects.filter(**request.session['proy_params'])

#verificcar que no existan parametros vacios
checkParams = lambda x: dict((k, v) for k,v in x.items() if x[k])

def resultado_detail(request, id):
    resultado = get_object_or_404(Resultado, id=id)    
    if request.method == 'POST':
        tabla_params = {}
        form = SubFiltroForm(request.POST)
        if form.is_valid():
            request.session['main'] = form.cleaned_data['main_var']
            for key in [a for a in form.cleaned_data.keys() if not a == 'main_var']:
                if form.cleaned_data[key]:
                    request.session['var2'] = (key, form.cleaned_data[key])
                    
            return HttpResponseRedirect('/proyecto/resultado/%s/output' % resultado.id)                                
    else:
        form = SubFiltroForm()                                             
    return render_to_response('contraparte/resultado_detail.html', RequestContext(request, locals()))

def output(request, id):
    query = _get_query(request)
    resultado = get_object_or_404(Resultado, id=id)    
    main_field = request.session['main']
    var2 = request.session['var2']    
    dicc = {}    
    relation = Actividad._meta.get_field_by_name(main_field)[0].rel.to    
    opts = relation.objects.all()    
    
    if var2[0] == 'evaluacion':
        opts2 = EVALUACION
        tipo = 'choice'
    values = eval(var2[0])    
    
    for meh in opts:
        dicc[meh] = {}        
        for foo in opts2:
            if tipo == 'choice':
                op = foo[0]
            dicc[meh][foo[1]] = query.filter(**{main_field:meh, values[var2[1]]:op})            
                            
    return render_to_response('contraparte/output.html', RequestContext(request, locals()))







