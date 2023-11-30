from django.db import models

class DmdDevices(models.Model):
    id = models.IntegerField(primary_key=True)
    serial_number = models.CharField(max_length=50)
    store_number = models.IntegerField()
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    st = models.CharField(max_length=50)
    zip = models.IntegerField()
    model = models.CharField(max_length=50)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dmd_devices'
