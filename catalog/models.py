from django.db import models

class Specialization(models.Model):
    specialization = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.specialization


class Hall(models.Model):
    hall = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.hall


class Master(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    at_work = models.BooleanField(default=False)
    halls = models.ManyToManyField(Hall, related_name='masters')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
