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
from tickets.models import Tickets, TicketsUsed
from uuid import UUID
from django.utils import timezone


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.
    
     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}
    
     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.
    
     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test

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

        is_found = False

        if is_valid_uuid(uuid):
        
            try:
                ticket = Tickets.objects.get(uuid=uuid)
                is_found = True
            except ObjectDoesNotExist:
                is_found = False
        
        if is_found:
            print("Ticket found: %s, %s", ticket.name, ticket.uuid)
            tickets_used = TicketsUsed.objects.filter(ticket=ticket, is_used=False).order_by('ticket_number')
            """
            try:
                tickets_used = TicketsUsed.objects.get(ticket=ticket, is_used=False).order_by('ticket_number').first()
                tickets_used.is_used = True
                tickets_used.time_used = timezone.now()
                tickets_used.save()
            except ObjectDoesNotExist:
                pass
            """

            if tickets_used:
                print(tickets_used[0])
                tickets_used[0].is_used = True
                tickets_used[0].time_used = timezone.now()
                tickets_used[0].save()

            """
                for ticket_used in tickets_used:
                    ticket_used.is_used = True
                    ticket_used.time_used = timezone.now()
                    ticket_used.save()
                    break
            """

            #return render(request, template_to_use, event_context)
            return render(request, "qr_ok.html")
            #return render(request, template_to_use)

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
