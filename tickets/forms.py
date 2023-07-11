from email.policy import default
from django import forms
from django.core.validators import RegexValidator
from .models import Tickets, TicketsClass

# member 
AMOUNT_CHOICES =( 
    (1, "1"), 
    (2, "2"), 
    (3, "3"), 
    (4, "4"), 
    (5, "5"), 
) 

class OrderForm(forms.Form):
    phone_regex = RegexValidator(regex=r'08([1-9])\d{7,14}', message="Nomor harus dalam format: '0899999999'. Minimal 10 dan maximal 15 digits.")
    nama = forms.CharField(label="Nama Lengkap Anda")
    email = forms.EmailField(
        label="Alamat Email Yang Masih Valid",
        #error_messages={"Mohon masukkan alamat email yang benar"}
    )
    phonenumber = forms.CharField(
        label="Nomor HP",
        validators=[phone_regex],
        max_length=20
    )
    ticket_class = forms.ModelChoiceField(
        label="Ticket Class",
        queryset=TicketsClass.objects.filter(),
        initial=18
    )
    amount = forms.ChoiceField(
        label="Jumlah Tiket",
        choices=AMOUNT_CHOICES,
        initial=1
    ) 
    
'''
class QueryQrForm(forms.Form):
    email = forms.EmailField(label="Alamat Email yang digunakan untuk mendaftar")
    event = forms.ModelChoiceField(
        label="Jadwal Ibadah yang Anda mendaftar",
        queryset=Event.objects.filter(is_active=True),
        widget=forms.RadioSelect()
    )
'''
