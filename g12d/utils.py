# -*- coding: utf-8 -*-

#ugly code but functional

to_choices = lambda x: [(y,unslugify(y)) for y in x]

def unslugify(value):
    return ' '.join([s.capitalize() \
                     if i == 0 else s \
                     for i, s in enumerate(value.split('_'))])