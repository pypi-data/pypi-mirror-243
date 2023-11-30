from django.db import models

class Image(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    device_image = models.BinaryField(blank=True, null=True)
    note = models.CharField()

    class Meta:
        managed = False
        db_table = 'image'
