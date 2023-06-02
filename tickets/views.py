from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.urls import reverse
from qr_code.qrcode.utils import QRCodeOptions
from .models import Tickets, TicketsUsed
from .wagtail_hooks import TicketsAdmin
from django.core.mail import EmailMessage
from django.conf import settings
import os
import requests


def qr_code(request, ticket_id):
    # Build context for rendering QR codes.
    context = dict(
        qr_options=QRCodeOptions(size='h', border=1, error_correction='L', version=3),
        ticket_id=ticket_id
    )

    # Render the view.
    return render(request, 'tickets/qr_ticket.html', context=context)


def authorize_ticket(request, ticket_id):
    url_helper = TicketsAdmin().url_helper
    print(ticket_id)
    try:
        ticket = Tickets.objects.get(uuid=ticket_id)
        ticket.authorization = True
        ticket.is_cleaned = True
        ticket.save()
    except ObjectDoesNotExist:
        pass

    return redirect(url_helper.index_url)


def mail_tickets(request, ticket_id):
    url_helper = TicketsAdmin().url_helper
    print(ticket_id)

    try:
        ticket = Tickets.objects.get(uuid=ticket_id, authorization=True)
        if ticket.email:
            all_tickets = TicketsUsed.objects.filter(ticket=ticket)
            subject = 'Ticket Konser'
            from_email = settings.EMAIL_HOST_USER
            body = ''
            email = EmailMessage(
                    subject=subject,
                    from_email=from_email,
                    body=body
                    )
            for each_ticket in all_tickets:
                ticket_filename = str(each_ticket.uuid) + '.png'
                ticket_filename_base = os.path.join(settings.TICKETS_FOLDER, ticket_filename)
                email.attach_file(str(ticket_filename_base))

            email.to = [ticket.email]
            print('Sending email to {}'.format(ticket.email))
            email.send()

    except ObjectDoesNotExist:
        pass

    return redirect(url_helper.index_url)


def telegram_image(image):
    apiToken = settings.TELEGRAM_TOKEN
    chatID = settings.TELEGRAM_GROUP_ID
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendPhoto'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'photo': image})
        print(response.text)
    except Exception as e:
        print(e)

def telegram_tickets(request, ticket_id):
    url_helper = TicketsAdmin().url_helper
    print(ticket_id)

    try:
        ticket = Tickets.objects.get(uuid=ticket_id, authorization=True)
        all_tickets = TicketsUsed.objects.filter(ticket=ticket)
        for each_ticket in all_tickets:
            ticket_filename = str(each_ticket.uuid) + '.png'
            ticket_filename_url = settings.WAGTAILADMIN_BASE_URL + settings.TICKETS_ROOT + ticket_filename
            telegram_image(ticket_filename_url)
            print('Sending image {}'.format(ticket_filename_url))

    except ObjectDoesNotExist:
        pass

    return redirect(url_helper.index_url)
