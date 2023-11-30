from django.db import models

class CountryCodes(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField()
    alpha_2_code = models.CharField()
    alpha_3_code = models.CharField()

    class Meta:
        managed = False
        db_table = 'country_codes'
