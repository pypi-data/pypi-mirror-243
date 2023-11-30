from django.db import models
from .tracking import Tracking
from .shipping_status import ShippingStatus
from .shipping_status_easypost import ShippingStatusEasypost

class TrackingStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    tracking = models.ForeignKey(Tracking, models.DO_NOTHING)
    checkpoint_order = models.IntegerField()
    detailed_status = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    status_date = models.DateTimeField()
    shipping_status = models.ForeignKey(ShippingStatus, models.DO_NOTHING)
    shipping_status_easypost = models.ForeignKey(ShippingStatusEasypost, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'tracking_status'
