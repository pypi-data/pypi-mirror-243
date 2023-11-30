from django.db import models

class Carrier(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    reference = models.CharField()
    carrier_id = models.CharField()
    type = models.CharField()
    description = models.CharField()
    carrier_type = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'carrier'
