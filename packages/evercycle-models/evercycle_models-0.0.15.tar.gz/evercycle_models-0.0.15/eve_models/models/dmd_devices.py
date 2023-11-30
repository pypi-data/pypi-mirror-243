from django.db import models

class DmdDevices(models.Model):
    id = models.IntegerField(primary_key=True)
    serial_number = models.CharField()
    store_number = models.IntegerField()
    contact = models.CharField()
    address = models.CharField()
    city = models.CharField()
    st = models.CharField()
    zip = models.IntegerField()
    model = models.CharField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dmd_devices'
