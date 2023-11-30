from django.db import models
from models.program import Program
from models.pricebook import Pricebook

class ProgramDeviceQuantity(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    program = models.ForeignKey(Program, models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=65535, decimal_places=65535)
    pricebook = models.ForeignKey(Pricebook, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'program_device_quantity'
