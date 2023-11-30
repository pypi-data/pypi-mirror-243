from django.db import models

class Carrier(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    reference = models.CharField(max_length=50)
    carrier_id = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    carrier_type = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'carrier'
