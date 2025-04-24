from django.db import models
from django.core.exceptions import ValidationError

class Specialization(models.Model):
    specialization = models.CharField(max_length=255, primary_key=True, unique=True)

    def __str__(self):
        return self.specialization


class Hall(models.Model):
    hall = models.CharField(max_length=10, primary_key=True, unique=True)

    def __str__(self):
        return self.hall


class Master(models.Model):
    master_id = models.CharField(max_length=10, primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    at_work = models.BooleanField(default=False)
    halls = models.ManyToManyField(Hall, related_name='masters')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Box(models.Model):
    number_box = models.PositiveIntegerField(primary_key=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='boxes')

    def __str__(self):
        return f"Box {self.number_box} in {self.hall}"


class Work(models.Model):
    id_work = models.CharField(max_length=7, primary_key=True, unique=True)
    time_on_work = models.DecimalField(max_digits=72, decimal_places=0)
    ready = models.BooleanField(default=False)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='works')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='works')
    allowed = models.BooleanField(default=False)

    def clean(self):
        if self.time_on_work < 0:
            raise ValidationError("Work time must be a positive number.")

    def __str__(self):
        return f"Work {self.id_work} by {self.master} - {self.specialization}"
