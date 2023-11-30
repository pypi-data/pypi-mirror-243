from django.db import models

class PyxeraFormData(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    reference = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    howlong = models.CharField(max_length=50)
    otherdevices = models.IntegerField()
    allowfollowup = models.BooleanField()
    serialnumber = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pyxera_form_data'
