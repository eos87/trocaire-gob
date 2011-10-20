# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models.loading import get_model
from django.utils import simplejson

def fill(request):
    #obtain all parameters
    model = request.GET.get('model', '')
    app_label = request.GET.get('app', '')
    filter = request.GET.get('filter', '')
    val = request.GET.get('val', '')
    regress = request.GET.get('regress', '')
    
    #make query
    objects = get_model(app_label, model).objects.filter(** {filter:val}).values(*regress.split(','))
            
    return HttpResponse(simplejson.dumps(list(objects)), mimetype="application/json")