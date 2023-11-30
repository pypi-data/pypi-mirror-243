from django.db import models

class Dispatched(models.Model):
    id = models.IntegerField(primary_key=True)
    case_number = models.IntegerField()
    case_created_date = models.CharField()
    intended_destination = models.CharField()
    user_s_name = models.CharField()
    notes = models.CharField(blank=True, null=True)
    line_address_1 = models.CharField()
    line_address_2 = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True)
    zipcode = models.IntegerField()
    asset_serial_number = models.CharField()
    outbound_tracking = models.CharField()
    inbound_tracking = models.IntegerField()
    processed = models.BooleanField()
    serial = models.CharField()

    class Meta:
        managed = False
        db_table = 'dispatched'
