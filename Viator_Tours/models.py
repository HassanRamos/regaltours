from django.db import models


class Viator_Destinations(models.Model):
    destination_name = models.CharField(max_length=250, unique=True, db_index=True)
    destination_id = models.IntegerField()
    destination_type =  models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.destination_name