from django.db import models
from models.flatfile_request import FlatfileRequest

class FlatfileUpload(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    flatfile_request = models.ForeignKey(FlatfileRequest, models.DO_NOTHING)
    contact = models.TextField()  # This field type is a guess.
    address = models.TextField()  # This field type is a guess.
    reference1 = models.CharField()
    reference2 = models.CharField()
    reference3 = models.CharField()
    device_info = models.TextField()  # This field type is a guess.
    checksum = models.CharField()
    program = models.ForeignKey('Program', models.DO_NOTHING)
    devices = models.TextField()  # This field type is a guess.
    serial_list = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'flatfile_upload'
