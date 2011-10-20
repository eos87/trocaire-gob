# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import RadioSelect
from trocaire.models import *
from contraparte.models import *
from formutils.forms import FormFKAutoFill    
from lugar.models import *
from utils import *  
 

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
#    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all())
#    municipio = forms.ModelChoiceField(queryset=Municipio.objects.all())
    
    
    class Foo:
        config = [{'on_change': {'field': 'organizacion'},
                   'fill': {'field': 'proyecto', 'model': 'Proyecto', 'app_label': 'contraparte'},
                   'values': {'filter': 'organizacion', 'regress': 'id,nombre'}}]

#--- parametros para creacion del form de cruces ----
first_class = {'tipo_actividad': ['tipo_actividad'], 
               'tema_actividad': ['tema_actividad'], 
               'ejes_transversales': ['ejes_transversales']}

participantes = {'participantes_por_sexo': ['hombres', 'mujeres'],
                 'participantes_por_edad': ['adultos', 'jovenes', 'ninos'],
                 'participantes_por_tipo': ['autoridades', 'maestros', 'lideres', 
                                            'pobladores', 'estudiantes', 'miembros']}

evaluacion = {'relevancia_del_tema': 'relevancia',
              'efectividad_de_la_accion': 'efectividad',
              'grado_de_efectividad': 'aprendizaje',
              'nivel_de_empoderamiento': 'empoderamiento',
              'evaluacion_de_participacion': 'participacion'}

recursos = {'comentarios': ['comentarios'],
            'acuerdos': ['acuerdos'],
            'fotos': ['foto1', 'foto2', 'foto3'],
            'video': ['video']}

tipo = {'participantes': 'sum', 'evaluacion': 'count'}        
    
class SubFiltroForm(forms.Form):
    main_var = forms.ChoiceField(choices=to_choices(first_class.keys()), 
                                 widget=RadioSelect(attrs={'class':'main'}))
    participantes = forms.ChoiceField(choices=to_choices(participantes.keys()), 
                                      widget=RadioSelect(attrs={'class':'unique'}),
                                      required=False)
    evaluacion = forms.ChoiceField(choices=to_choices(evaluacion.keys()), 
                                   widget=RadioSelect(attrs={'class':'unique'}),
                                   required=False)
    recursos = forms.ChoiceField(choices=to_choices(recursos.keys()), 
                                 widget=RadioSelect(attrs={'class':'unique'}),
                                 required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        participantes = cleaned_data.get("participantes")
        evaluacion = cleaned_data.get("evaluacion")
        recursos = cleaned_data.get("recursos")

        if not participantes and not evaluacion and not recursos:              
            #validando que se marque una segunda variable         
            raise forms.ValidationError("Debes elegir al menos una segunda variable "
                        "a cruzar. Ejm: Participantes o Evaluacion o Recursos")
            
        if (participantes and evaluacion) or (participantes and recursos) or (evaluacion and recursos):
            #validando que solo se elija una segunda variable         
            raise forms.ValidationError("Solo puede seleccionar una segunda variable")
                            
        
        return cleaned_data        



