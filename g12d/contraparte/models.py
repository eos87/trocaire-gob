# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from trocaire.models import *
from lugar.models import Municipio, Comunidad
from smart_selects.db_fields import ChainedForeignKey 

SI_NO = ((1, u'Si'), (2, u'No'))

class Proyecto(models.Model):
    organizacion = models.ForeignKey(Organizacion)
    nombre = models.CharField(max_length=250)
    codigo = models.CharField(max_length=20)
    inicio = models.DateField()
    finalizacion = models.DateField()
    monto_trocaire = models.IntegerField()
    monto_contrapartida = models.IntegerField()
    contacto = models.CharField(max_length=100, verbose_name='Persona de contacto')
    aporta_trocaire = models.IntegerField(choices=SI_NO, verbose_name=u'Aporta a Trocaire')
    municipios = models.ManyToManyField(Municipio)    
    
    def __unicode__(self):
        return u'%s - %s' % (self.organizacion.nombre_corto, self.codigo)
    
    class Meta:
        verbose_name_plural = u'Proyectos'
        
class Resultado(models.Model):    
    nombre_corto = models.CharField(max_length=50)
    descripcion = models.TextField()
    aporta_a = models.ForeignKey(ResultadoPrograma)
    proyecto = models.ForeignKey(Proyecto)
    
    def __unicode__(self):
        return u'%s' % self.nombre_corto
    
    class Meta:
        verbose_name = u'Resultado del proyecto'
        verbose_name_plural = u'Resultados de proyectos' 
        
class Organizador(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __unicode__(self):
        return u'%s' % self.nombre
    
    class Meta:
        verbose_name_plural = u'Organizadores'
        
TIPO_ACTIVIDAD = ((1, u'Encuentro'), (2, u'Taller'),
                  (3, u'Cabildo'), (4, u'Reunión Comunitaria'),
                  (5, u'Campamento'), (6, u'Festival'),
                  (7, u'Feria'), (8, u'Gestión ante autoridades'),
                  (9, u'Diplomado'))

TEMA_ACTIVIDAD = ((1, u'Derechos Humanos'), (2, u'Empoderamiento'),
                  (3, u'Participación Cuidadana'), (4, u'Incidencia'),
                  (5, u'Marco Jurídico Nacional'), (6, u'Género'),
                  (7, u'Fortalecimiento de capacidades de la organización'))

EJES = ((1, u'Interculturalidad'), (2, u'Género'), 
        (3, u'Medio ambiente'), (4, u'Generacional'))

EVALUACION = ((99, u'No aplica'), (1, u'Muy malo'), (2, u'Malo'), 
              (3, u'Regular'), (4, u'Bueno'), (5, u'Muy bueno'))

class Actividad(models.Model):
    organizacion = models.ForeignKey(Organizacion)
    proyecto = ChainedForeignKey(Proyecto, 
                                 chained_field="organizacion",
                                 chained_model_field="organizacion", 
                                 show_all=False,
                                 auto_choose=True)    
    persona_organiza = models.ForeignKey(Organizador)
    nombre_actividad = models.CharField(max_length=150)
    fecha = models.DateTimeField()
    municipio = ChainedForeignKey(Municipio, 
                                 chained_field="proyecto",
                                 chained_model_field="proyecto", 
                                 show_all=False,
                                 auto_choose=True)    
    comunidad = ChainedForeignKey(Comunidad, 
                                 chained_field="municipio",
                                 chained_model_field="municipio", 
                                 show_all=False,
                                 auto_choose=True)
    tipo_actividad = models.ForeignKey(TipoActividad)
    tema_actividad = models.ForeignKey(Tema)
    ejes_transversales = models.ForeignKey(EjeTransversal)
    #participantes por sexo
    hombres = models.IntegerField(default=0)
    mujeres = models.IntegerField(default=0)
    #participantes por edad
    no_dato = models.BooleanField(verbose_name='No hay datos')
    adultos = models.IntegerField(default=0, verbose_name=u'Adultos/as')
    jovenes = models.IntegerField(default=0, verbose_name=u'Jóvenes')
    ninos = models.IntegerField(default=0, verbose_name=u'Niños/as')
    #participantes por tipo
    no_dato1 = models.BooleanField(verbose_name='No hay datos')
    autoridades = models.IntegerField(default=0, verbose_name=u'Autoridades públicas')
    maestros = models.IntegerField(default=0)
    lideres = models.IntegerField(default=0, verbose_name=u'Lideres/zas Comunitarios')
    pobladores = models.IntegerField(default=0, verbose_name=u'Pobladores/as')
    estudiantes = models.IntegerField(default=0)
    miembros = models.IntegerField(default=0, verbose_name=u'Miembros de Org Copartes')
    resultado = ChainedForeignKey(Resultado, 
                                  chained_field="proyecto",
                                  chained_model_field="proyecto", 
                                  show_all=False,
                                  auto_choose=True,
                                  verbose_name=u'Resultado al que aporta')    
    #evaluaciones
    relevancia = models.IntegerField(choices=EVALUACION, verbose_name=u'Relevancia del tema/acción')
    efectividad = models.IntegerField(choices=EVALUACION, verbose_name='Efectividad de la acción')
    aprendizaje = models.IntegerField(choices=EVALUACION, verbose_name=u'Grado de efectividad')
    empoderamiento = models.IntegerField(choices=EVALUACION, verbose_name=u'Nivel de empoderamiento')
    participacion = models.IntegerField(choices=EVALUACION, verbose_name=u'Evaluación de participación')
    #recursos
    comentarios = models.TextField(blank=True, default='')
    acuerdos = models.TextField(blank=True, default='')
    foto1 = models.ImageField(upload_to='fotos', blank=True, null=True)
    foto2 = models.ImageField(upload_to='fotos', blank=True, null=True)
    foto3 = models.ImageField(upload_to='fotos', blank=True, null=True)
    video = models.CharField(max_length=300, blank=True, default='')
    
    def __unicode__(self):
        return u'%s - %s' % (self.nombre_actividad, self.fecha)
    
    def clean(self):
        suma_base = self.hombres + self.mujeres
        suma_edad = self.adultos + self.jovenes + self.ninos
        suma_tipo = self.autoridades + self.maestros + self.lideres + self.pobladores + self.estudiantes + self.miembros
        
        if not self.no_dato:
            if suma_base != suma_edad:
                raise ValidationError('La suma de los participantes por edad no concuerda')
            
        if not self.no_dato1:
            if suma_base != suma_tipo:
                raise ValidationError('La suma de los participantes por tipo no concuerda')
    
    class Meta:
        verbose_name_plural = u'Actividades' 
       
    
    
    
    
       