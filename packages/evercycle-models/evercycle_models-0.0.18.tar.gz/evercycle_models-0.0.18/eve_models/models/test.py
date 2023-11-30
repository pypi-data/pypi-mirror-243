from django.db import models

class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    field = models.IntegerField()
    csv = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'
