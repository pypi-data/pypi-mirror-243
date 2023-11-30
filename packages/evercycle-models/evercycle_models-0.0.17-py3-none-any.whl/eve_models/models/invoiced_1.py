from django.db import models

class Invoiced1(models.Model):
    id = models.IntegerField(primary_key=True)
    request_uid = models.CharField(max_length=50)
    organization = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    device_count = models.IntegerField()
    date_ticket_requested = models.CharField(max_length=50)
    date_delivered_by_carrier = models.CharField(max_length=50)
    return_tracking = models.IntegerField()
    outbound_tracking = models.IntegerField()
    package = models.CharField(max_length=50)
    contact_first_name = models.CharField(max_length=50)
    contact_last_name = models.CharField(max_length=50)
    contact_address = models.CharField(max_length=50)
    device_types = models.CharField(max_length=50)
    serials = models.CharField(blank=True, null=True)
    note = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoiced_1'
