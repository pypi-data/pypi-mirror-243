from django.db import models

class GeolocationData(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField()
    country = models.CharField(blank=True, null=True)
    country_iso3 = models.CharField(max_length=50)
    postal_code = models.CharField(blank=True, null=True)
    city = models.CharField(blank=True, null=True)
    state = models.CharField(blank=True, null=True)
    state_abbr = models.CharField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    longitude = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geolocation_data'