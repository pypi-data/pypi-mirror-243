from django.db import models

class Pdf(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    cod_id = models.CharField()
    audit = models.ForeignKey(Audit, models.DO_NOTHING)
    status = models.CharField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pdf'
