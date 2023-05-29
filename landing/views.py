from django.shortcuts import render
from .models import Verse
from random import choice
from tickets.models import Tickets


def landing(request):
    pks = Verse.objects.values_list('pk', flat=True)
    random_pk = choice(pks)
    random_verse = Verse.objects.get(pk=random_pk)
    
    return render(request, 'landing.html', {'verse': random_verse })


def counter(request):
    ticket_all = Ticket.objects.all().count()
    ticket_count = Tickets.objects.filter(is_used=True).count()

    return render(request, 'counter.html', {'ticket_count': ticket_count, 'ticket_all': ticket_all})


    
