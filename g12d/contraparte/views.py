# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.db.models.loading import get_model
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
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
            #almacenando variable principal en session
            request.session['main'] = form.cleaned_data['main_var']
            for key in [a for a in form.cleaned_data.keys() if not a in ['main_var', 'total', 'bar_graph', 'pie_graph']]:
                if form.cleaned_data[key]:
                    #almacenando variable dos en session
                    request.session['var2'] = (key, form.cleaned_data[key])
            
            request.session['total'] = True if form.cleaned_data['total'] else False            
            request.session['bar_graph'] = True if form.cleaned_data['bar_graph'] else False
            request.session['pie_graph'] = True if form.cleaned_data['pie_graph'] else False                                                                                       
                    
            return HttpResponseRedirect('/proyecto/resultado/%s/output' % resultado.id)                                
    else:
        form = SubFiltroForm()
        
        #eliminando las variables de session
        for a in ['var2', 'main', 'total', 'bar_graph', 'pie_graph']:
            if a in request.session:
                del request.session[a]
                                            
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
    elif var2[0] == 'participantes':
        opts2 = eval(var2[0])[var2[1]]
        tipo = 'sum'
    
    for meh in opts:
        dicc[meh] = {}
        qs = query.filter(resultado=resultado, **{main_field:meh})        
        for foo in opts2:
            if tipo == 'choice':
                op = foo[0]
                dicc[meh][foo[1]] = qs.filter(**{values[var2[1]]:op})
            elif tipo == 'sum':  
                suma = qs.aggregate(campo_sum=Sum(foo))['campo_sum']
                dicc[meh][foo] = suma or 0
                
    url = request.GET.get('url', '')
    if url != '':
        
        return HttpResponse(url)               
                            
    return render_to_response('contraparte/output.html', RequestContext(request, locals()))







