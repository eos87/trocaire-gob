# -*- coding: utf-8 -*-
from django import template
register = template.Library()

#-------- begin inclusion tags ------------
@register.inclusion_tag('contraparte/load_table.html')
def load_table(dicc, opts2, request, tipo):    
    return { 'dicc' : dicc,
            'opts2': opts2,
            'request': request,
            'tipo': tipo}
    
@register.inclusion_tag('contraparte/bar_graph.html')
def bar_graph(dicc, var2, main_field, tipo):    
    return { 'dicc' : dicc,
            'var2': var2,
            'main_field': main_field,
            'tipo': tipo}
    
@register.inclusion_tag('contraparte/pie_graph.html')
def pie_graph(dicc, var2, main_field, tipo):    
    return { 'dicc' : dicc,
            'var2': var2,
            'main_field': main_field,
            'tipo': tipo}

#---------- end inclusion tags ---------------
    
#---------- other filter and tags ------------
@register.filter
def unslugify(value):
    return ' '.join([s.capitalize() \
                     if i == 0 else s \
                     for i, s in enumerate(value.split('_'))])
    
@register.filter
def get_value(dicc, key):   
    '''donde dicc es el diccionario con valores y key la llave a obtener'''
    return dicc[key] 

@register.filter
def total_dict_query(value):    
    return sum([x.count() for x in value.values()])

@register.filter
def total_dict(value):    
    return sum(value.values())

@register.filter
def total_per_key(value, arg):
    '''value es el dict y arg es el key del que se quiere obtener el total o suma'''   
    return sum([v[arg] for v in value.values()])

@register.filter
def total_per_query_key(value, arg):
    '''value es el dict y arg es el key del que se quiere obtener el total o suma'''   
    return sum([v[arg].count() for v in value.values()])

@register.filter
def total_general(tabla, qs=None):   
    '''donde tabla es un dicc donde estan todos los valores'''    
    if qs==1:
        return sum([sum(len(a) for a in value.values()) for value in tabla.values()])       
    return sum([sum(value.values()) for value in tabla.values()]) 

