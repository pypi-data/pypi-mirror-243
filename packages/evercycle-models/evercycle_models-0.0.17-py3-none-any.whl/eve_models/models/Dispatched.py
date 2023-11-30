from django.db import models

class Dispatched(models.Model):
    id = models.IntegerField(primary_key=True)
    case_number = models.IntegerField()
    case_created_date = models.CharField(max_length=50)
    intended_destination = models.CharField(max_length=50)
    user_s_name = models.CharField(max_length=50)
    notes = models.CharField(blank=True, null=True)
    line_address_1 = models.CharField(max_length=50)
    line_address_2 = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True)
    zipcode = models.IntegerField()
    asset_serial_number = models.CharField(max_length=50)
    outbound_tracking = models.CharField(max_length=50)
    inbound_tracking = models.IntegerField()
    processed = models.BooleanField()
    serial = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dispatched'
