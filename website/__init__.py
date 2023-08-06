from django.template.defaulttags import register
from math import ceil
import json

@register.filter(name='times')
def times(number):
    return range(number)

@register.filter(name='group')
def group(_array):

    batch = []
    sub_batch = []
    for idx , hotel  in enumerate(_array):
        hotel["MinHotelPrice"]["TotalPrice"] = hotel["MinHotelPrice"]["@TotalPrice"]

        if idx % 2 == 0:
            if idx != 0:
                batch.append(sub_batch)
            sub_batch = []
            sub_batch.append(json.loads(json.dumps(hotel)))
        else:
            if idx == len(_array)-1:
                batch.append(sub_batch)
            sub_batch.append(json.loads(json.dumps(hotel)))
    return(json.dumps({"batch":batch}))
