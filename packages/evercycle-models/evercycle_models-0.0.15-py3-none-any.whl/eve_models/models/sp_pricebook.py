from django.db import models
from models.service_provider import ServiceProvider

class SpPricebook(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    service_provider = models.ForeignKey(ServiceProvider, models.DO_NOTHING)
    grade_scale = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sp_pricebook'
