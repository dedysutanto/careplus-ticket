from django.shortcuts import render
from .models import Verse
from random import choice


def landing(request):
    pks = Verse.objects.values_list('pk', flat=True)
    random_pk = choice(pks)
    random_verse = Verse.objects.get(pk=random_pk)
    
    return render(request, 'landing.html', {'verse': random_verse })


    
