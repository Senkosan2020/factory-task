from django.db import models

class Specialization(models.Model):
    specialization = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.specialization


class Hall(models.Model):
    hall = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.hall
