from django.db import models
from models.address import Address

class Processor(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    address = models.ForeignKey(Address, models.DO_NOTHING)
    main_contact_name = models.CharField()
    main_contact_email = models.CharField()
    main_contact_phone = models.CharField()
    warehouse_auth_id = models.CharField()
    warehouse_id_ret = models.IntegerField()
    warehouse_id_out = models.IntegerField()
    warehouse_id_nofill = models.CharField()
    warehouse_id_ret_test = models.IntegerField()
    warehouse_id_out_test = models.IntegerField()
    contact_id = models.IntegerField()
    address_0 = models.TextField(db_column='address')  # Field renamed because of name conflict. This field type is a guess.
    contact = models.TextField()  # This field type is a guess.
    easypost_address_id = models.CharField()
    easypost_address_id_test = models.CharField()

    class Meta:
        managed = False
        db_table = 'processor'
