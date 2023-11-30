from django.db import models

class Invoiced2(models.Model):
    id = models.IntegerField(primary_key=True)
    request_uid = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'invoiced_2'
