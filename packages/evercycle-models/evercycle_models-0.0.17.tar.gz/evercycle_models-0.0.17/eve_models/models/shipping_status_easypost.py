from django.db import models

class ShippingStatusEasypost(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    status_id = models.IntegerField()
    general_status = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'shipping_status_easypost'
