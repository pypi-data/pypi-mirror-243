from django.db import models

class ShippingStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    general_status = models.CharField()

    class Meta:
        managed = False
        db_table = 'shipping_status'
