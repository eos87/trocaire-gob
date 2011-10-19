# -*- coding: utf-8 -*-
from django import forms
from trocaire.models import *
from contraparte.models import *
from formutils.forms import FormFKAutoFill       

class ProyectoForm(FormFKAutoFill):
    organizacion = forms.ModelChoiceField(queryset=Organizacion.objects.all())
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all())    
    
    class Media:        
        js = ('js/autofill.js',)
        
    class Foo:
        config = [{'on_change': {'field': 'organizacion', 'model': 'Proyecto', 'app_label': 'contraparte'},
               'fill': {'field': 'proyecto', 'model': 'Proyecto', 'app_label': 'contraparte'} 
               },
                {'on_change': {'field': 'proyecto', 'model': 'Organizacion', 'app_label': 'trocaire'},
               'fill': {'field': 'proyecto', 'model': 'Proyecto', 'app_label': 'contraparte'}}
               ]

def buscar(request):
    print 'LRDL'