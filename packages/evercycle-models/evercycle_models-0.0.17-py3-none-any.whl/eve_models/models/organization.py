from django.db import models
from .address import Address
from .contact import Contact

class Organization(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    address = models.ForeignKey(Address, models.DO_NOTHING)
    parent_org = models.ForeignKey('self', models.DO_NOTHING, db_column='parent_org')
    main_contact = models.ForeignKey(Contact, models.DO_NOTHING)
    tax_id = models.CharField(max_length=50)
    updated_by = models.IntegerField()
    updated_at = models.DateTimeField()
    logo_image = models.BinaryField(blank=True, null=True)
    address_0 = models.TextField(db_column='address')  # Field renamed because of name conflict. This field type is a guess.
    contact = models.TextField()  # This field type is a guess.
    organization_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    logo = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'organization'
