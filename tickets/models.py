import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


class Tickets(models.Model):
    name = models.CharField(
            _('Ticket Name'),
            max_length=20)
    uuid = models.UUIDField(
            _('Ticket ID'),
            default = uuid.uuid4, 
            editable=False)
    is_used = models.BooleanField(
            _('Is Used'),
            default=False,
            editable=False)

    class Meta:
        db_table = 'tickets'
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return self.name

    def qr_ticket(self):
        text = format_html('<a href="../qr_code/' + str(self.uuid) + '/" target="_blank"><img src="../../static/tickets/qr.png"></a>')
        return text

    """
    def save(self, *args, **kwargs):
        self.name = self.uuid
        super(Tickets, self).save(*args, **kwargs)
    """

