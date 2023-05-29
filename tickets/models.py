import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    def __str__(self):
        return self.name

    """
    def save(self, *args, **kwargs):
        self.name = self.uuid
        super(Tickets, self).save(*args, **kwargs)
    """

