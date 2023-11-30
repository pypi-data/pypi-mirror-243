from django.db import models

class PackageType(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    description = models.CharField()
    dimension = models.TextField()  # This field type is a guess.
    processor = models.ForeignKey('Processor', models.DO_NOTHING)
    capacity = models.IntegerField()
    easypost_parcel_id = models.CharField()
    easypost_parcel_id_test = models.CharField()

    class Meta:
        managed = False
        db_table = 'package_type'
