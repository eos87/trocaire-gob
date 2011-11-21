# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from g12d.contraparte.views import checkParams
from g12d.forms import *

def filtro_programa(request):
    params = {}
    filtro = {}
    if request.method == 'POST':
        form = ProgramaForm(request.POST)
        if form.is_valid():
            params['organizacion__id__in'] = form.cleaned_data['organizaciones'].values_list('id', flat=True)
            try:            
                params['proyecto__id__in'] = form.cleaned_data['proyectos'].values_list('id', flat=True)
            except:
                params['proyecto__id__in'] = None
            params['resultado__aporta_a__id'] = form.cleaned_data['resultado'].id            
            params['mes__in'] = form.cleaned_data['meses']
            params['fecha__year'] = form.cleaned_data['anio']
            
            #guardando los filtros seleccionados para pintarlos en plantilla
            filtro['organizacion'] = form.cleaned_data['organizaciones']
            filtro['proyecto'] = form.cleaned_data['proyectos']
            filtro['meses'] = form.cleaned_data['meses']
            filtro['year'] = form.cleaned_data['anio']
            filtro['salida'] = 'Por programa'
            
            params = checkParams(params)
            request.session['filtro'] = filtro
            request.session['params'] = params             
            
            return HttpResponseRedirect('/variables/')            
    else:
        form = ProgramaForm()
    return render_to_response('trocaire/filtro_programa.html', RequestContext(request, locals()))