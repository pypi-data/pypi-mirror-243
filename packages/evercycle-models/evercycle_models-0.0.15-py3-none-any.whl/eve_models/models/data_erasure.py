from django.db import models

class DataErasure(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField()
    website_url = models.CharField()
    certificate_example = models.BinaryField(blank=True, null=True)
    certifications = models.TextField()  # This field type is a guess.
    policy = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_erasure'
