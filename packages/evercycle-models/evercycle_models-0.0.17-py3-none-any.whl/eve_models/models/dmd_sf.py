from django.db import models

class DmdSf(models.Model):
    id = models.IntegerField(primary_key=True)
    asset_contact_contact_id = models.CharField(max_length=50)
    asset_contact_full_name = models.CharField(max_length=50)
    asset_name = models.CharField(max_length=50)
    asset_transaction_number = models.CharField(max_length=50)
    disposal_only = models.BooleanField()
    open_transactions = models.CharField(max_length=50)
    type_of_asset = models.CharField(blank=True, null=True)
    asset_contact_mailing_country = models.CharField(max_length=50)
    date_returned = models.CharField(blank=True, null=True)
    case_number = models.IntegerField()
    address = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    error = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'dmd_sf'
