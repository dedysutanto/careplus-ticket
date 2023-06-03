import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageDraw
from .models import Tickets, TicketsUsed
from django.conf import settings



def generate_qr(uuid):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=2,
    )
    qr.add_data(uuid)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_folder = 'media/qr'
    qr_folder_base = os.path.join(settings.BASE_DIR, qr_folder)
    #os.mkdir(qr_folder_base)
    try:
        os.makedirs(qr_folder_base)
    except FileExistsError:
        pass
    qr_filename = uuid + '.png'
    qr_filename_base = os.path.join(qr_folder_base, qr_filename)
    img.save(qr_filename_base)

    return qr_filename_base


def generate_ticket(uuid):

    try:
        os.makedirs(settings.TICKETS_FOLDER)
    except FileExistsError:
        pass

    qr_src = generate_qr(uuid)
    ticket_img_base = Image.open(settings.BASE_TICKET_SRC)
    qr_img_base = Image.open(qr_src)
    ticket_img_base.paste(qr_img_base,(250, 380))
    ticket_filename = uuid + '.png'
    ticket_filename_base = os.path.join(settings.TICKETS_FOLDER, ticket_filename)
    ticket_img_base.save(ticket_filename_base)
    
    return ticket_filename_base


def create_ticket(ticket):
    ticket_filename = generate_ticket(str(ticket.uuid))
    img = Image.open(ticket_filename)
    # Call draw Method to add 2D graphics in an image
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(settings.FONT_SRC_BASE, size=32)
 
    # Add Text to an image
    text = ticket.ticket.name + ' - ' + ticket.ticket.ticket_class_child.__str__() + ' - ' + str(ticket.ticket_number)

    if ticket.ticket.ticket_class_child is None:
        text = ticket.ticket.name + ' - ' + ticket.ticket.ticket_class.__str__() + ' - ' + str(ticket.ticket_number)

    draw.text((280, 360), text, font=font, fill=(0, 0, 0))
    img.save(ticket_filename)

