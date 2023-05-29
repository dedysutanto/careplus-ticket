from django.shortcuts import render
from qr_code.qrcode.utils import QRCodeOptions

def qr_code(request, ticket_id):
    # Build context for rendering QR codes.
    context = dict(
        qr_options=QRCodeOptions(size='h', border=1, error_correction='L'),
        ticket_id=ticket_id
    )

    # Render the view.
    return render(request, 'tickets/qr_ticket.html', context=context)
