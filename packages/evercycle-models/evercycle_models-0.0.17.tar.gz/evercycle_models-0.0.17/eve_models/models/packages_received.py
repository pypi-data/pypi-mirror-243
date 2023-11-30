from django.db import models

class PackagesReceived(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    request = models.ForeignKey('Request', models.DO_NOTHING)
    received = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'packages_received'
