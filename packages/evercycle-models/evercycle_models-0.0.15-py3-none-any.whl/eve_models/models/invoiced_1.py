from django.db import models

class Invoiced1(models.Model):
    id = models.IntegerField(primary_key=True)
    request_uid = models.CharField()
    organization = models.CharField()
    program = models.CharField()
    device_count = models.IntegerField()
    date_ticket_requested = models.CharField()
    date_delivered_by_carrier = models.CharField()
    return_tracking = models.IntegerField()
    outbound_tracking = models.IntegerField()
    package = models.CharField()
    contact_first_name = models.CharField()
    contact_last_name = models.CharField()
    contact_address = models.CharField()
    device_types = models.CharField()
    serials = models.CharField(blank=True, null=True)
    note = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoiced_1'
