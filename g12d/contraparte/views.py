# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.db.models.loading import get_model
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.models import Site
from g12d.forms import *
from models import *
import short
import datetime


def filtro_proyecto(request):
    proy_params = {}
    filtro = {}
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proy_params['organizacion__id'] = form.cleaned_data['organizacion'].id
            proy_params['proyecto__id'] = form.cleaned_data['proyecto'].id
            proy_params['mes__in'] = form.cleaned_data['meses']
            proy_params['fecha__year'] = form.cleaned_data['anio']
            
            #guardando los filtros seleccionados para pintarlos en plantilla
            filtro['organizacion'] = [form.cleaned_data['organizacion'], ]
            filtro['proyecto'] = [form.cleaned_data['proyecto'], ]
            filtro['meses'] = form.cleaned_data['meses']
            filtro['year'] = form.cleaned_data['anio']
            
            proy_params = checkParams(proy_params)
            request.session['filtro'] = filtro
            request.session['proy_params'] = proy_params 
            
            resultados = Resultado.objects.filter(proyecto__id=proy_params['proyecto__id'])            
    else:
        form = ProyectoForm()
            
    return render_to_response('contraparte/filtro.html', RequestContext(request, locals()))

def _get_query(params):        
    return Actividad.objects.filter(**params)

#verificcar que no existan parametros vacios
checkParams = lambda x: dict((k, v) for k, v in x.items() if x[k])

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

def output(request, id, saved_params=None):    
    total = request.session['total']
    #chequear si no se trara de una salida guardada y reasignar variables    
    if saved_params:        
        params = saved_params['proy_params']
        main_field = saved_params['main']
        var2 = saved_params['var2']
    else:
        filtro = request.session['filtro']
        params = request.session['proy_params']
        main_field = request.session['main']
        var2 = request.session['var2']
        
    query = _get_query(params)
    resultado = get_object_or_404(Resultado, id=id)    
    dicc = {}    
    relation = Actividad._meta.get_field_by_name(main_field)[0].rel.to    
    opts = relation.objects.all()    
    
    """Aca inicia el guardado de la la salida, generamiento de url y reporte"""
    url = request.GET.get('url', '')
    comment = request.GET.get('comment', '')
    save = request.GET.get('save', '')
    if url != '':
        #guardando la session y generar URL
        params = {}
        params['main'] = request.session['main']
        params['var2'] = request.session['var2']
        params['proy_params'] = request.session['proy_params']
        params['total'] = True if request.session['total'] else False
        params['bar_graph'] = True if request.session['bar_graph'] else False
        params['pie_graph'] = True if request.session['pie_graph'] else False
        params['resultado__id'] = resultado.id
        
        obj, created = Output.objects.get_or_create(params=str(params),
                                           date=datetime.date.today(),
                                           user=request.user)        
        if save == '1':
            obj.file = True
            if comment:
                obj.comment = comment
        obj.time = datetime.datetime.time(datetime.datetime.now())
        obj.save()        
        return HttpResponse('%s/i/%s' % (Site.objects.all()[0].domain, obj._hash()))
    
    #creacion del diccionario con los datos de la tabla
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
                
    #si es una salida guardada retornar valores aqui         
    if saved_params:
        return locals()
                               
    return render_to_response('contraparte/output.html', RequestContext(request, locals()))

def shortview(request, hash):
    saved_out = get_object_or_404(Output, id=short.decode_url(hash))    
    #obteniendo los parametros de la salida guardada o compartida y luego el query
    params = eval(saved_out.params)    
    
    #extrayendo los filtros seleccionados
    if 'organizacion__id' in params['proy_params']:
        orgs = [params['proy_params']['organizacion__id']]
        proys = [params['proy_params']['proyecto__id']]             
    elif 'organizacion__id__in' in params['proy_params']:
        orgs = params['proy_params']['organizacion__id__in']
        proys = params['proy_params']['proyecto__id__in']   
    
    #llamando a la vista encargada de generar el dicc
    variables = output(request, params['resultado__id'], params)
    
    variables['filtro'] = {'organizacion': Organizacion.objects.filter(id__in=orgs),
                           'proyecto': Proyecto.objects.filter(id__in=proys),
                           'meses': params['proy_params']['mes__in'],
                           'year': params['proy_params']['fecha__year'],
                           }
    variables['noshare'] = True   
           
    return render_to_response('contraparte/output.html', RequestContext(request, variables))





