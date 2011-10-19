# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models.loading import get_model

def fill(request):
    model = request.GET.get('model', '')
    app_label = request.GET.get('app', '')
    value = get_model(app_label, model).objects.all()
    print value
    return HttpResponse ('LPM')