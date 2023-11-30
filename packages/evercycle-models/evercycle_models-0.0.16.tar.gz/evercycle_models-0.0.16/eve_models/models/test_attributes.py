from django.db import models

class TestAttributes(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    attributes = models.TextField()  # This field type is a guess.
    list_enums = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'test_attributes'
