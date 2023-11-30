from django.db import models
from .program import Program

class Request(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    program = models.ForeignKey(Program, models.DO_NOTHING)
    created_by = models.IntegerField()
    reference = models.CharField(max_length=50)
    request_type = models.ForeignKey('RequestType', models.DO_NOTHING)
    processed = models.BooleanField()
    address = models.TextField()  # This field type is a guess.
    contact_list = models.TextField()  # This field type is a guess.
    request_type_0 = models.TextField(db_column='request_type')  # Field renamed because of name conflict. This field type is a guess.
    pickup_info = models.TextField()  # This field type is a guess.
    updated_by = models.IntegerField()
    updated_at = models.DateTimeField()
    serial_list = models.TextField()  # This field type is a guess.
    disposition_list = models.TextField()  # This field type is a guess.
    deleted = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'request'