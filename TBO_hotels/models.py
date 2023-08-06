from django.db import models


class TBO_Country(models.Model):
    country_name = models.CharField(max_length=250, unique=True, db_index=True)
    country_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country_name


class TBO_City(models.Model):
    city_name = models.CharField(max_length=250)
    city_code = models.CharField(max_length=10, primary_key=True, db_index=True)
    country = models.ForeignKey(TBO_Country,on_delete=models.CASCADE,to_field="country_name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city_name