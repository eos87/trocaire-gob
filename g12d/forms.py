# -*- coding: utf-8 -*-
from django import forms
from trocaire.models import *
from contraparte.models import *
from formutils.forms import FormFKAutoFill       

MONTH_CHOICES = (('', 'Mes'),
                 (1, 'Enero'), (2, 'Febrero'),
                 (3, 'Marzo'), (4, 'Abril'),
                 (5, 'Mayo'), (6, 'Junio'),
                 (7, 'Julio'), (8, 'Agosto'),
                 (9, 'Septiembre'), (10, 'Octubre'),
                 (11, 'Noviembre'), (12, 'Diciembre'))

ANIOS_CHOICE = (('', u'Año'), (2010, 2010), (2011, 2011), (2012, 2012), )

class ProyectoForm(FormFKAutoFill):
    organizacion = forms.ModelChoiceField(queryset=Organizacion.objects.all())
    proyecto = forms.ModelChoiceField(queryset=Proyecto.objects.all())
    meses = forms.MultipleChoiceField(choices=MONTH_CHOICES, error_messages={'required': 'Seleccione al menos un mes'}, required=False)    
    anio = forms.ChoiceField(choices=ANIOS_CHOICE, error_messages={'required': u'Seleccione un año'}, required=False, label=u'Año')
        
    class Foo:
        config = [{'on_change': {'field': 'organizacion'},
                   'fill': {'field': 'proyecto', 'model': 'Proyecto', 'app_label': 'contraparte'},
                   'values': {'filter': 'organizacion', 'regress': 'id,nombre'}},]