from .detect import *
from .alert import *
from .relief import *


def feedback_list(request, instance):
    if instance == "covid":
        alertlist = Location.objects.filter(covid_status=1)
    elif instance == "flood":
        alertlist = Location.objects.filter(flood_status=1)
    elif instance == "fire":
        alertlist = Location.objects.filter(fire_status=1)
    if len(alertlist) == 0:
        alertlist = None
    return render(request, instance+'/feedback.html', {'al': alertlist, 'instance': instance})
