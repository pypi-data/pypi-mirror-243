from django.db import models

class RequestType(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'request_type'
