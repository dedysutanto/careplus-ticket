from datetime import timedelta
from ssl import SSL_ERROR_WANT_CONNECT
from urllib import request
from django.shortcuts import render, redirect
from django.conf import settings 
from .forms import PinForm
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from .models import Pin
from tickets.models import Tickets


# Seat Number
def get_seat(start, value):

    seat_no = ""
    for x in range(start, start+value):
        seat_no += str(x) + ", " 
    
    return seat_no[:len(seat_no)-2]    


@csrf_exempt
def qr_scan(request):
    if request.POST:
        uuid = request.POST.get('id', None)
        force_checkin = request.POST.get('force_checkin', None)
        #print(registrantid)
        
        try:
            ticket = Tickets.objects.get(uuid=uuid)
            is_found = True
        except ObjectDoesNotExist:
            is_found = False
        
        if is_found:
            uuid.is_used = True
            uuid.save()

            #return render(request, template_to_use, event_context)
            return render(request, template_to_use)

        else:
            return render(request, "qr_not_found.html")

    return HttpResponseNotFound("404")


def pin_entry(request):
    p = Pin.objects.get(id=1)
    #PIN = "778899"
    PIN = p.pin
    pin_salah = ''
    if request.POST:
        form = PinForm(request.POST)

        if form.is_valid():
            pin = form.cleaned_data['pin']

            if pin == PIN:
                #scanner_uri = static('qrscan/scanner/index.html')
                request.session['is_pin'] = 'OK'
                return render(request, "scanner.html")
            else:
                pin_salah = 'PIN yang Anda masukan salah'

    form = PinForm()

    return render(request, "pin_entry.html", {'form': form, 'pin_salah': pin_salah})


def scanner(request):
    return render(request, 'scanner.html')