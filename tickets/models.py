import uuid
from django.contrib.admin.filters import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models.signals import post_save, post_delete, post_init
from django.dispatch import receiver
from django.core.validators import RegexValidator
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageDraw
from django.conf import settings
from django.core.mail import send_mail
import requests
import urllib.parse


def telegram_msg(message):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage?chat_id={settings.TELEGRAM_GROUP_ID}&text={message}"
    print(requests.get(url).json()) # this sends the message


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
    ticket_img_base.paste(qr_img_base,(253, 370))
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
    text1 = ticket.ticket.name
    text2 = ticket.ticket.ticket_class_child.__str__() + ' - ' + str(ticket.ticket_number) + '/' + str(ticket.ticket.amount)

    if ticket.ticket.ticket_class_child is None:
        text1 = ticket.ticket.name
        text2 = ticket.ticket.ticket_class.__str__() + ' - ' + str(ticket.ticket_number) + '/' + str(ticket.ticket.amount)

    draw.text((285, 360), text1, font=font, fill=(0, 0, 0))
    draw.text((285, 870), text2, font=font, fill=(0, 0, 0))
    img.save(ticket_filename)



class TicketsClass(models.Model):
    name = models.CharField(
            _('Class Name'),
            max_length=20,
            )
    price = models.IntegerField(blank=True, default=0)

    seats = models.IntegerField(
            _('Number of Seats'),
            default=0,
            )
    seats_sell = models.IntegerField(
            _('Seats Sold'),
            default=0,
            editable=False
            )
    description = models.TextField(
            _('Description'),
            blank=True,
            null=True
            )

    class Meta:
        db_table = 'tickets_class'
        verbose_name = 'Ticket Class'
        verbose_name_plural = 'Tickets Class'

    def __str__(self):
        return self.name

    def seats_available(self):
        return self.seats - self.seats_sell
    seats_available.short_description = 'Seats Avail'

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(TicketsClass, self).save(*args, **kwargs)


class TicketsClassChild(models.Model):
    parent_class = models.ForeignKey(
            TicketsClass,
            on_delete=models.CASCADE,
            blank=True,
            default=None
            )
    name = models.CharField(
            _('Class Name'),
            max_length=20,
            )
    minimal_promise = models.IntegerField(
            _('Minimal Promise'),
            default=0
            )
    description = models.TextField(
            _('Description'),
            blank=True,
            default=None
            )

    class Meta:
        db_table = 'tickets_class_child'
        verbose_name = 'Ticket Class Plus'
        verbose_name_plural = 'Tickets Class Plus'

    def __str__(self):
        return f'{self.parent_class.name} {self.name}'

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(TicketsClassChild, self).save(*args, **kwargs)


class Tickets(models.Model):
    phone_regex = RegexValidator(regex=r'^\0?1?\d{9,16}$', message="Phone number must be entered in the format: '0899999999'. Up to 16 digits allowed.")
    name = models.CharField(
            _('Ticket Name'),
            max_length=30)
    uuid = models.UUIDField(
            _('Ticket ID'),
            default = uuid.uuid4, 
            editable=False)
    phonenumber = models.CharField(
            _('WA Number'),
            blank=True,
            max_length=20,
            validators=[phone_regex],
            )
    email = models.EmailField(blank=True)
    amount = models.IntegerField(
            _('Ticket Amount'),
            default=1
            )
    faith_promise = models.IntegerField(
            _('Faith Promise'),
            default=0,
            )
    ticket_class = models.ForeignKey(
            TicketsClass,
            verbose_name=_('Ticket Class'),
            on_delete=models.RESTRICT,
            )

    ticket_class_child = models.ForeignKey(
            TicketsClassChild,
            verbose_name=_('Ticket Class Plus'),
            on_delete=models.RESTRICT,
            blank=True,
            null=True,
            )

    created_at = models.DateTimeField(
            auto_now=True,
            )
    authorization = models.BooleanField(
            _('Authorized'),
            default=False,
            )
    description = models.TextField(
            blank=True,
            )

    class Meta:
        db_table = 'tickets'
        verbose_name = 'Ticket Sell'
        verbose_name_plural = 'Tickets Sell'

    def __str__(self):
        return self.name

    def qr_ticket(self):
        text = format_html('<a href="../../tickets/qr_code/' + str(self.uuid) + '/" target="_blank"><img src="../../static/tickets/qr.png"></a>')
        return text
    qr_ticket.short_description = 'QR Ticket'

    def clean(self):
        self.is_cleaned = True
       
        if self.authorization == False:
            if self.pk is not None:
                initial_ticket = Tickets.objects.get(pk=self.pk)
                ticket_class = TicketsClass.objects.get(id=initial_ticket.ticket_class.id)
                if self.ticket_class == initial_ticket.ticket_class:
                    self.ticket_class.seats_sell = self.ticket_class.seats_sell - initial_ticket.amount
                else:
                    ''' If Change Class, return back previous ticket class seats '''
                    ticket_class.seats_sell = ticket_class.seats_sell = initial_ticket.amount
                    ticket_class.save()
                    

            if self.ticket_class.seats_sell + self.amount > self.ticket_class.seats:
                seats_available = self.ticket_class.seats - self.ticket_class.seats_sell
                error_text = 'Tickets hanya tersisa {}'.format(str(seats_available))
                raise ValidationError(
                        {'amount':[error_text]}
                        )

            if self.ticket_class_child is not None:
                if self.faith_promise == 0 or self.faith_promise < self.ticket_class_child.minimal_promise:
                    error_text = 'Harap masuukan jumlah Janji Iman. Minimal {}'.format(str(self.ticket_class_child.minimal_promise))
                    raise ValidationError(
                            {'faith_promise': [error_text]},
                        )

            if self.faith_promise != 0:
                if self.ticket_class_child is None:
                    raise ValidationError(
                            {'ticket_class_child': ['Harap masukkan Ticket Class Plus sesuai dengan Janji Iman']},
                        )

        super(Tickets, self).clean()


    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        self.name = self.name.upper()
        super(Tickets, self).save(*args, **kwargs)


class TicketsUsed(models.Model):
    ticket = models.ForeignKey(
            Tickets,
            on_delete=models.CASCADE,
            )

    uuid = models.UUIDField(
            _('Ticket ID'),
            default = uuid.uuid4, 
            editable=False)

    ticket_number = models.IntegerField(
            _('Ticket Number'),
            default=0
            )
    time_used = models.DateTimeField(
            auto_now_add=True,
            blank=True,
            editable=False,
            )
    is_used = models.BooleanField(
            _('Is Used'),
            default=False,
            editable=False,
            )

    class Meta:
        db_table = 'tickets_used'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return self.ticket.name

    def qr_ticket(self):
        text = format_html('<a href="../../tickets/qr_code/' + str(self.uuid) + '/" target="_blank"><img src="../../static/tickets/qr.png"></a>')
        #text = format_html('<a href="../../media/tickets/' + str(self.uuid) + '/" target="_blank"><img src="../../static/tickets/qr.png"></a>')
        return text
    qr_ticket.short_description = 'QR Ticket'


@receiver(post_save, sender=Tickets)
def create_ticketsused(sender, created, instance, **kwargs):
    tickets_used = TicketsUsed.objects.filter(ticket=instance)
    for ticket_used in tickets_used:
        ticket_filename = str(ticket_used.uuid) + '.png'
        ticket_filename_base = os.path.join(settings.TICKETS_FOLDER, ticket_filename)
        try:
            os.remove(ticket_filename_base)
        except FileNotFoundError:
            pass
        ticket_used.delete()

    if instance.authorization:
        for i in range(instance.amount):
            ticketsused = TicketsUsed()
            ticketsused.ticket = instance
            ticketsused.name = instance.name
            ticketsused.ticket_number = i + 1
            ticketsused.save()
            create_ticket(ticketsused)

        if instance.ticket_class_child is None:
            text = 'TICKET AUTHORIZED!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nSeats: ' + str(instance.amount)
        else:
            text = 'TICKET AUTHORIZED!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nClass Plus: ' + str(instance.ticket_class_child) + '\nSeats: ' + str(instance.amount)
        msg = urllib.parse.quote(text)
        telegram_msg(msg)

@receiver(post_save, sender=Tickets)
def reduce_seats_sell(sender, created, instance, **kwargs):
    tickets_count = 0
    tickets = Tickets.objects.filter(ticket_class=instance.ticket_class)
    for ticket in tickets:
        tickets_count = tickets_count + ticket.amount

    tickets_class = TicketsClass.objects.get(id=instance.ticket_class.id)
    tickets_class.seats_sell = tickets_count
    tickets_class.save()
    print('receiver->reduce_seats_sell {} {}'.format(tickets_class, tickets_class.seats_sell))

    if created:
        if instance.ticket_class_child is None:
            text = 'NEW SELLING!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nSeats: ' + str(instance.amount)
        else:
            text = 'NEW SELLING!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nClass Plus: ' + str(instance.ticket_class_child) + '\nSeats: ' + str(instance.amount)
    else:
        if instance.ticket_class_child is None:
            text = 'UPDATE SELLING!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nSeats: ' + str(instance.amount)
        else:
            text = 'UPDATE SELLING!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nClass Plus: ' + str(instance.ticket_class_child) + '\nSeats: ' + str(instance.amount)

    msg = urllib.parse.quote(text)
    telegram_msg(msg)


@receiver(post_delete, sender=Tickets)
def add_seats_sell(sender, instance, **kwargs):
    tickets_count = 0
    tickets = Tickets.objects.filter(ticket_class=instance.ticket_class)
    for ticket in tickets:
        tickets_count = tickets_count + ticket.amount

    tickets_class = TicketsClass.objects.get(id=instance.ticket_class.id)
    tickets_class.seats_sell = tickets_count
    tickets_class.save()

    if instance.ticket_class_child is None:
        text = 'DELETE SELLING!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nSeats: ' + str(instance.amount)
    else:
        text = 'DELETE SELLING!\nName: ' + str(instance.name) + '\nClass: ' + str(instance.ticket_class) + '\nClass Plus: ' + str(instance.ticket_class_child) + '\nSeats: ' + str(instance.amount)

    msg = urllib.parse.quote(text)
    telegram_msg(msg)
