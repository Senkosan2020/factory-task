from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Specialization(models.Model):
    specialization = models.CharField(max_length=255, primary_key=True, unique=True)
    number = models.PositiveIntegerField(
        validators=[
            MinValueValidator(10),
            MaxValueValidator(99)
        ]
    )

    def __str__(self):
        return self.specialization

    def clean(self):
        if self.number % 5 != 0:
            raise ValidationError({'number': 'Number must be divisible by 5.'})


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

    def clean(self):
        if len(self.master_id) != 10:
            raise ValidationError("master_id must be exactly 10 characters long.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Box(models.Model):
    number_box = models.PositiveIntegerField(primary_key=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='boxes')

    def __str__(self):
        return f"Box {self.number_box} in {self.hall}"


class Work(models.Model):
    id_work = models.CharField(max_length=7, primary_key=True, unique=True)
    time_on_work = models.DecimalField(max_digits=7, decimal_places=0)
    ready = models.BooleanField(default=False)
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name='works')
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='works')

    def clean(self):
        if len(self.id_work) != 7:
            raise ValidationError("id_work must be exactly 7 characters long.")

        if self.time_on_work != 7:
            raise ValidationError("time_on_work must be exactly 7 characters long.")

    def __str__(self):
        return f"Work {self.id_work} by {self.master} - {self.specialization}"

    def get_preparing_minutes(self):
        str_time = str(int(self.time_on_work)).zfill(7)
        return int(str_time[:2])

    def get_work_minutes(self):
        str_time = str(int(self.time_on_work)).zfill(7)
        return round(int(str_time[2:]) / 60)


class Worker(models.Model):
    worker_id = models.CharField(max_length=10, primary_key=True, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    specializations = models.ManyToManyField(Specialization, related_name='workers')
    box = models.ForeignKey(Box, on_delete=models.PROTECT, related_name='workers')
    works = models.ManyToManyField(Work, related_name='workers', blank=True)
    at_work = models.BooleanField(default=False)

    def clean(self):
        if len(self.worker_id) != 10:
            raise ValidationError("worker_id must be exactly 10 characters long.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
