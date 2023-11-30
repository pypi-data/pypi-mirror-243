from django.db import models

class Delivered(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracking_number = models.CharField(max_length=50)
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'delivered'
