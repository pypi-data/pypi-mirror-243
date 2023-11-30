from django.db import models

class PackageType(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    dimension = models.TextField()  # This field type is a guess.
    processor = models.ForeignKey('Processor', models.DO_NOTHING)
    capacity = models.IntegerField()
    easypost_parcel_id = models.CharField(max_length=50)
    easypost_parcel_id_test = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'package_type'
