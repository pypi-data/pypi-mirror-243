from django.db import models

class FlatfileRequest(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    batch_id = models.CharField(max_length=50)
    user_id = models.IntegerField()
    program = models.ForeignKey('Program', models.DO_NOTHING)
    total_rows = models.IntegerField()
    uploaded = models.BooleanField()
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'flatfile_request'