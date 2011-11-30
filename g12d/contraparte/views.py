# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.db.models.loading import get_model
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.models import Site
from django.utils import simplejson
from g12d.forms import *
from g12d import short
from g12d.settings import EXPORT_SERVER
from models import *
import datetime
import thread

@login_required
def filtro_proyecto(request):
    proy_params = {}
    filtro = {}
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request=request)
        if form.is_valid():
            proy_params['organizacion__id'] = form.cleaned_data['organizacion'].id
            proy_params['proyecto__id'] = form.cleaned_data['proyecto'].id 
            proy_params['resultado__id'] = form.cleaned_data['resultado'].id           
            proy_params['mes__in'] = form.cleaned_data['meses']
            proy_params['fecha__year'] = form.cleaned_data['anio']
            
            #guardando los filtros seleccionados para pintarlos en plantilla
            filtro['organizacion'] = [form.cleaned_data['organizacion'], ]
            filtro['proyecto'] = [form.cleaned_data['proyecto'], ]
            filtro['meses'] = form.cleaned_data['meses']
            filtro['year'] = form.cleaned_data['anio']
            filtro['salida'] = 'Por proyecto'
            filtro['resultado'] = form.cleaned_data['resultado'].nombre_corto
            
            proy_params = checkParams(proy_params)
            request.session['filtro'] = filtro
            request.session['params'] = proy_params            
            
            return HttpResponseRedirect('/variables/')            
    else:
        form = ProyectoForm(request=request)
            
    return render_to_response('contraparte/filtro.html', RequestContext(request, locals()))

def _get_query(params):        
    return Actividad.objects.filter(**params)

#verificcar que no existan parametros vacios
checkParams = lambda x: dict((k, v) for k, v in x.items() if x[k])

@login_required
def variables(request):
    filtro = request.session['filtro']        
    if request.method == 'POST':
        tabla_params = {}
        form = SubFiltroForm(request.POST)
        if form.is_valid():
            #almacenando variable principal en session
            request.session['main'] = form.cleaned_data['main_var']
            for key in [a for a in form.cleaned_data.keys() if not a in ['main_var', 'total', 'bar_graph', 'pie_graph', 'eval_tipo']]:
                if form.cleaned_data[key]:
                    #almacenando variable dos en session
                    if form.cleaned_data['eval_tipo'] == '2' and key == 'evaluacion':
                        request.session['var2'] = ('%s_m' % key, form.cleaned_data[key])
                        print request.session['var2']                        
                    else:
                        request.session['var2'] = (key, form.cleaned_data[key])
                                    
            request.session['total'] = True if form.cleaned_data['total'] else False            
            request.session['bar_graph'] = True if form.cleaned_data['bar_graph'] else False
            request.session['pie_graph'] = True if form.cleaned_data['pie_graph'] else False 
            if form.cleaned_data['evaluacion']:
                request.session['eval_tipo'] = 'Mujeres' if form.cleaned_data['eval_tipo'] == 2 else 'Hombres'
            else:
                request.session['eval_tipo'] = None
                    
            return HttpResponseRedirect('/variables/output/')                                
    else:
        form = SubFiltroForm()
        
        #eliminando las variables de session
        for a in ['var2', 'main', 'total', 'bar_graph', 'pie_graph', 'eval_tipo']:
            if a in request.session:
                del request.session[a]
                                            
    return render_to_response('contraparte/variables.html', RequestContext(request, locals()))

def output(request, saved_params=None):   
    #chequear si no se trara de una salida guardada y reasignar variables    
    if saved_params:        
        total = saved_params['total']
        params = saved_params['params']
        main_field = saved_params['main']
        var2 = saved_params['var2']
    else:
        total = request.session['total']
        filtro = request.session['filtro']
        params = request.session['params']
        main_field = request.session['main']
        var2 = request.session['var2']
        eval_tipo = request.session['eval_tipo']
        
    query = _get_query(params)        
    dicc = {}    
    relation = Actividad._meta.get_field_by_name(main_field)[0].rel.to    
    opts = relation.objects.all()
    sitio = Site.objects.all()[0]      
    
    #Aca inicia el guardado de la la salida, generamiento de url y reporte    
    if request.method == 'POST':        
        url = request.POST.get('url', '')
        comment = request.POST.get('comment', None)
        save = request.POST.get('save', None)
        bar_svg = request.POST.get('bar_svg', None)
        pie1_svg = request.POST.get('pie1_svg', None)
        pie2_svg = request.POST.get('pie2_svg', None)        
        if url != '':
            #guardando la session y generar URL
            params = {}
            params['main'] = request.session['main']
            params['var2'] = request.session['var2']
            params['params'] = request.session['params']
            params['total'] = True if request.session['total'] else False
            params['bar_graph'] = True if request.session['bar_graph'] else False
            params['pie_graph'] = True if request.session['pie_graph'] else False
            params['salida'] = request.session['filtro']['salida'] 
            params['eval_tipo'] = request.session['eval_tipo']
            params['resultado'] = request.session['filtro']['resultado']
            
            obj, created = Output.objects.get_or_create(params=str(params),
                                               date=datetime.date.today(),
                                               user=request.user)        
            if save == '1':
                obj.file = True
                if comment:                
                    obj.comment = comment
                if bar_svg:
                    thread.start_new_thread(get_graph_png, (bar_svg, obj, 'bar_img'))                    
                if pie1_svg:
                    thread.start_new_thread(get_graph_png, (pie1_svg, obj, 'pie1_img', 450))                    
                if pie2_svg:
                    thread.start_new_thread(get_graph_png, (pie2_svg, obj, 'pie2_img', 450))                  
                                     
            obj.time = datetime.datetime.time(datetime.datetime.now())        
            obj.save()        
            return HttpResponse('%s/i/%s' % (sitio.domain, obj._hash()))
    
    #creacion del diccionario con los datos de la tabla
    if var2[0] in ['evaluacion','evaluacion_m']:
        opts2 = EVALUACION
        tipo = 'choice'
        values = eval(var2[0])
    elif var2[0] == 'participantes':
        opts2 = eval(var2[0])[var2[1]]
        tipo = 'sum'
    
    for meh in opts:
        dicc[meh.nombre] = {}
        qs = query.filter(**{main_field:meh})        
        for foo in opts2:
            if tipo == 'choice':
                op = foo[0]
                dicc[meh.nombre][foo[1]] = qs.filter(**{values[var2[1]]:op})
            elif tipo == 'sum':  
                suma = qs.aggregate(campo_sum=Sum(foo))['campo_sum']
                dicc[meh.nombre][foo] = suma or 0
                
    #si es una salida guardada retornar valores aqui         
    if saved_params:
        return {'dicc': dicc, 'opts': opts, 'opts2': opts2, 'tipo': tipo, 'total': total,
                'var2': var2, 'main_field': main_field}
    
    #codigo para solicitar detalles    
    k = request.GET.get('k', '')
    k2 = request.GET.get('k2', '')
    data = request.GET.get('data', '')
    if k and k2:
        lista = []
        for obj in Actividad.objects.filter(id__in=[a.id for a in dicc[k][k2]]):
            #armar el json a retornar
            if data == 'multimedia':                
                lista.append(dict(nombre_actividad=obj.nombre_actividad, id=obj.id, foto1_thumb=obj.foto1.url_128x96,
                                  foto2_thumb=obj.foto2.url_128x96, foto3_thumb=obj.foto3.url_128x96, 
                                  foto1_pic=obj.foto1.url_640x480, foto2_pic=obj.foto2.url_640x480, foto3_pic=obj.foto3.url_640x480, 
                                  comunidad__nombre=obj.comunidad.nombre, municipio__nombre=obj.municipio.nombre, vthumb=obj.get_vthumb(),
                                  video=obj.get_video(), fecha=obj.fecha.strftime('%d/%m/%Y')))
            elif data == 'comentarios':
                lista.append(dict(nombre_actividad=obj.nombre_actividad, id=obj.id, comentarios=obj.comentarios,
                                  acuerdos=obj.acuerdos, comunidad__nombre=obj.comunidad.nombre, 
                                  municipio__nombre=obj.municipio.nombre, fecha=obj.fecha.strftime('%d/%m/%Y')))
        return HttpResponse(simplejson.dumps(lista), mimetype="application/json")
                               
    return render_to_response('contraparte/output.html', RequestContext(request, locals()))

#dejo esta funcion solo para explicar como funciona el lambda de abajo XD date2json
def date_to_json(param):     
    lista = []        
    for dicc in param:
        foo = {}
        for key, value in dicc.items():
            if type(value) == datetime.datetime:
                value = value.strftime('%Y-%m-%dT%H:%M:%S')
            foo[key] = value
        lista.append(foo)
    return lista

date2json = lambda x: map(lambda a: {k:v.strftime('%Y-%m-%dT%H:%M:%S') if type(v) == datetime.datetime else v for k, v in a.items()}, x) 

def shortview(request, hash):
    saved_out = get_object_or_404(Output, id=short.decode_url(hash))    
    #obteniendo los parametros de la salida guardada o compartida y luego el query
    params = eval(saved_out.params)    
    
    #extrayendo los filtros seleccionados
    if 'organizacion__id' in params['params']:
        orgs = [params['params']['organizacion__id']]
        proys = [params['params']['proyecto__id']]             
    elif 'organizacion__id__in' in params['params']:
        orgs = params['params']['organizacion__id__in']
        proys = params['params'].get('proyecto__id__in', [-1,])   
    
    #llamando a la vista encargada de generar el dicc
    variables = output(request, params)
    
    variables['filtro'] = {'organizacion': Organizacion.objects.filter(id__in=orgs),
                           'proyecto': Proyecto.objects.filter(id__in=proys),
                           'meses': params['params'].get('mes__in', None),
                           'year': params['params'].get('fecha__year', None),
                           'salida': params['salida'],
                           'resultado': params['resultado']
                           }
        
    variables['noshare'] = True
    variables['main_field'] = params['main']
    for key in ['total', 'bar_graph', 'pie_graph', 'var2', 'eval_tipo']:
        variables[key] = params[key]
           
    return render_to_response('contraparte/output.html', RequestContext(request, variables))

def get_proyectos(request):
    ids = request.GET.get('ids', '')
    if ids:
        try:
            ids = ids.split(',')
            proyectos = Proyecto.objects.filter(organizacion__id__in=map(int, ids),
                                                aporta_trocaire=1).values('id', 'organizacion__nombre_corto', 'codigo')
            print proyectos
        except Exception as e:
            print e
            return HttpResponse(e)
    else:
        return HttpResponse(':(')
    return HttpResponse(simplejson.dumps(list(proyectos)), mimetype="application/json")

def get_salidas(request):
    sitio = Site.objects.all()[0].domain    
    lista = []    
    #obtener las salidas guardadas por el usuario
    if request.user.is_authenticated():
        salidas = Output.objects.filter(user=request.user, file=True)
        for obj in salidas:
            lista.append(dict(id=obj.id, comment=obj.comment, date=obj.date.strftime('%d/%m/%Y'), hash=obj.hash))             
    return HttpResponse(simplejson.dumps(lista), mimetype="application/json")

def generate_report(request):
    if request.method == 'POST':
        ids = request.POST['ids']  
        salidas = Output.objects.filter(id__in=map(int, ids.split(',')), user=request.user)
        lista = []
        for salida in salidas:
            dicc = output(request, eval(salida.params))
            dicc['comment'] = salida.comment
            dicc['bar_img'] = salida.bar_img
            dicc['pie1_img'] = salida.pie1_img
            dicc['pie2_img'] = salida.pie2_img
            lista.append(dicc)
        
        response = render_to_response('report.html', {'lista': lista})
        response['Content-Disposition'] = 'attachment; filename=reporte.doc'    
        response['Content-Type'] = 'application/msword'
        response['Charset'] ='UTF-8'
        return response
    else:
        ids = request.GET.get('ids', '')
        delete = request.GET.get('e', None)
        if delete == 'ok':
            Output.objects.filter(id__in=map(int, ids.split(',')), user=request.user).delete()
            return HttpResponse('Reportes eliminados correctamente!')
                
        return render_to_response('report.html', RequestContext(request, {'lista': lista}))
    
def get_graph_png(svg, obj, field, width=940):
    import urllib
    data_dict = {'svg': svg, 'type': 'image/png', 'width': width, 'img_url': '1', 'filename': 'chart'}
    
    server_data = urllib.urlencode(data_dict)
    response = urllib.urlopen(EXPORT_SERVER, data = server_data)    
    setattr(obj, field, response.read()) 
    obj.save()
    return response.read()
    