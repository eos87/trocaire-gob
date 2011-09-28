# -*- coding: utf-8 -*-
from django.db import models
from trocaire.models import *
from lugar.models import Municipio
from django.forms import forms

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