from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
from uno.models import *
from twilio.rest import Client

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


twilio_account_sid = 'AC5ea8bb59991689451ceaf29ade8f320e'
twilio_auth_token = '7094c5b698252c3f9ab86103d2b22f23'
client = Client(twilio_account_sid, twilio_auth_token)


def alert_list(request, instance):
    if instance == "covid":
        alertlist = Location.objects.filter(covid_status=1)
    elif instance == "flood":
        alertlist = Location.objects.filter(flood_status=1)
    elif instance == "fire":
        alertlist = Location.objects.filter(fire_status=1)
    if len(alertlist) == 0:
        alertlist = None
    return render(request, instance+'/alert.html', {'al': alertlist, 'instance': instance})


@csrf_exempt
def send_alert(request):
    med = request.POST.get("med")
    sub = request.POST.get("subject")
    body = request.POST.get("body")
    res = {"msg": None, "email": None}

    users = User.objects.all()
    for user in users:
        if "e" in med and user.email is not None:
            email = EmailMessage(
                sub, body, from_email="hariharanr.sc73@gmail.com", to=[user.email]
            )
            email.send()

        if "s" in med and user.phone is not None:
            message = client.messages.create(
                body=body,
                from_='+12057518316',
                to='+91'+str(user.phone)
            )
            if message.error_code is None:
                res["msg"] = True
            else:
                res["msg"] = False

    return JsonResponse(res)
