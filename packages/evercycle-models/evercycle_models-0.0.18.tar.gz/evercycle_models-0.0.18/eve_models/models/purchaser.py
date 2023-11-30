from django.db import models

class Purchaser(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    address = models.TextField()  # This field type is a guess.
    contact = models.TextField()  # This field type is a guess.
    website = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'purchaser'
