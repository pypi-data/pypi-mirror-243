from django.db import models

class DmdSf(models.Model):
    id = models.IntegerField(primary_key=True)
    asset_contact_contact_id = models.CharField()
    asset_contact_full_name = models.CharField()
    asset_name = models.CharField()
    asset_transaction_number = models.CharField()
    disposal_only = models.BooleanField()
    open_transactions = models.CharField()
    type_of_asset = models.CharField(blank=True, null=True)
    asset_contact_mailing_country = models.CharField()
    date_returned = models.CharField(blank=True, null=True)
    case_number = models.IntegerField()
    address = models.CharField()
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.CharField()
    phone = models.CharField()
    address1 = models.CharField()
    address2 = models.CharField()
    city = models.CharField()
    state = models.CharField()
    postal_code = models.CharField()
    error = models.CharField()
    serial_number = models.CharField()
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'dmd_sf'
