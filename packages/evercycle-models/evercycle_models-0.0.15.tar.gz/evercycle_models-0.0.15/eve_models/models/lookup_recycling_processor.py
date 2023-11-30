from django.db import models

class LookupRecyclingProcessor(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    county_fips = models.CharField()
    state = models.CharField()
    county_name = models.CharField()
    processor = models.ForeignKey('Processor', models.DO_NOTHING)
    program = models.ForeignKey('Program', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'lookup_recycling_processor'
