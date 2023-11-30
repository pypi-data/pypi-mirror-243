from django.db import models

class LookupRecyclingProcessor(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    county_fips = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    county_name = models.CharField(max_length=50)
    processor = models.ForeignKey('Processor', models.DO_NOTHING)
    program = models.ForeignKey('Program', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lookup_recycling_processor'
