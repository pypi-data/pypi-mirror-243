from django.db import models


class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    created_by = models.IntegerField()
    location_name = models.CharField()
    address1 = models.CharField()
    address2 = models.CharField()
    city = models.CharField()
    state = models.CharField()
    postal_code = models.CharField()
    country = models.CharField()
    organization = models.ForeignKey('Organization', models.DO_NOTHING)
    updated_by = models.IntegerField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'address'