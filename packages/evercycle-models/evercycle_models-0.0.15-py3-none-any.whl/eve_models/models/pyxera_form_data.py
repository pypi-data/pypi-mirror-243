from django.db import models

class PyxeraFormData(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    reference = models.CharField()
    notes = models.CharField()
    address1 = models.CharField()
    address2 = models.CharField()
    city = models.CharField()
    state = models.CharField()
    postal_code = models.CharField()
    country = models.CharField()
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.CharField()
    phone = models.CharField()
    howlong = models.CharField()
    otherdevices = models.IntegerField()
    allowfollowup = models.BooleanField()
    serialnumber = models.CharField()
    tracking_number = models.CharField()

    class Meta:
        managed = False
        db_table = 'pyxera_form_data'
