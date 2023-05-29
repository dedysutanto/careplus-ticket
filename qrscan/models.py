from django.db import models


class Pin(models.Model):
    pin = models.CharField(max_length=6, default='778899')

    class Meta:
        db_table = 'pin'
        verbose_name = 'PIN'
        verbose_name_plural = 'PIN'

    def __str__(self):
        return 'PIN'
