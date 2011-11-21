# -*- coding: utf-8 -*-
from django.contrib import admin
from g12d.contraparte.models import *
from django import forms

class ResultadoInline(admin.TabularInline):
    model = Resultado
    extra = 1
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        # This method will turn all TextFields into giant TextFields
        if isinstance(db_field, models.TextField):
            return forms.CharField(label=u'Descripción', 
                                   widget=forms.Textarea(attrs={'cols': 60, 'rows':4, 'class': 'docx'}))
        return super(ResultadoInline, self).formfield_for_dbfield(db_field, **kwargs)


class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'organizacion', 'inicio', 'finalizacion', 'contacto']
    filter_horizontal = ['municipios']
    inlines = [ResultadoInline, ]
    

admin.site.register(Proyecto, ProyectoAdmin)
admin.site.register(Resultado)
admin.site.register(Organizador)

class ActividadAdmin(admin.ModelAdmin):
    list_filter = ['nombre_actividad', 'organizacion', 'proyecto', 'persona_organiza', 'fecha']
    search_fields = ['nombre_actividad', 'organizacion__nombre_corto', 'persona_organiza__nombre']
    list_display = ['nombre_actividad', 'organizacion', 'proyecto', 'fecha', 'resultado']
    
    fieldsets = [
        (None, {'fields': [('organizacion', 'proyecto'), 'persona_organiza', 'nombre_actividad', 'fecha',
                           'municipio', 'comunidad']}),
        ('Tipo, tema y ejes de actividad', {'fields': ['tipo_actividad', 'tema_actividad', 'ejes_transversales']}),
        ('Participantes por sexo', {'fields': [('hombres', 'mujeres'),]}),
        ('Participantes por edad', {'fields': [('adultos', 'jovenes', 'ninos', 'no_dato'),]}),
        ('Participantes por tipo', {'fields': [('autoridades', 'maestros', 'lideres', 'no_dato1'), 
                                               ('pobladores', 'estudiantes', 'miembros')]}),
        (None, {'fields': ['resultado',]}),
        ('Evaluacion', {'fields': [('relevancia', 'efectividad'), ('aprendizaje', 'empoderamiento'), 'participacion']}),
        ('Recursos', {'fields': [('foto1', 'foto2', 'foto3'), 'video', ('comentarios', 'acuerdos')]}),                                                          
    ]
    
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'cols': 50, 'rows':4, 'class': 'docx'})},        
    }
    
    def get_form(self, request, obj=None, ** kwargs):
        if request.user.is_superuser:        
            form = super(ActividadAdmin, self).get_form(request, ** kwargs)
        else:
            form = super(ActividadAdmin, self).get_form(request, ** kwargs)
            form.base_fields['organizacion'].queryset = request.user.organizacion_set.all()            
            #form.base_fields['proyecto'].queryset = request.user.organizacion_set.all()                        
        return form
    
    class Media:
        js = ('/files/js/actividad.js', )        
    
admin.site.register(Actividad, ActividadAdmin)

class OutputAdmin(admin.ModelAdmin):
    list_display = ['_hash', 'date', 'time']
    
admin.site.register(Output, OutputAdmin)    
    
    