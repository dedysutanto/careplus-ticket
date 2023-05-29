from django.db import models

# Create your models here.

class Verse(models.Model):
    ayat = models.CharField(max_length=300)
    pasal = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        db_table = "verse"
        verbose_name_plural = "Verses"