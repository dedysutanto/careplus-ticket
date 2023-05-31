import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class TicketsClass(models.Model):
    name = models.CharField(
            _('Class Name'),
            max_length=20,
            )
    price = models.IntegerField(blank=True, default=0)

    class Meta:
        db_table = 'tickets_class'
        verbose_name = 'Ticket Class'
        verbose_name_plural = 'Tickets Class'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(TicketsClass, self).save(*args, **kwargs)


class Tickets(models.Model):
    phone_regex = RegexValidator(regex=r'^\0?1?\d{9,16}$', message="Phone number must be entered in the format: '0899999999'. Up to 16 digits allowed.")
    name = models.CharField(
            _('Ticket Name'),
            max_length=20)
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
    ticket_class = models.ForeignKey(
            TicketsClass,
            on_delete=models.RESTRICT,
            )

    created_at = models.DateTimeField(
            auto_now=True,
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

    '''
    def save(self, *args, **kwargs):
        super(Tickets, self).save(*args, **kwargs)
    '''


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
        return text
    qr_ticket.short_description = 'QR Ticket'


@receiver(post_save, sender=Tickets)
def create_ticketsused(sender, created, instance, **kwargs):
    TicketsUsed.objects.filter(ticket=instance).delete()
    for i in range(instance.amount):
        ticketsused = TicketsUsed()
        ticketsused.ticket = instance
        ticketsused.ticket_number = i + 1
        ticketsused.save()

