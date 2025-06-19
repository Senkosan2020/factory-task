import pytest
from django.core.exceptions import ValidationError
from catalog.models import Specialization, Master, Worker, Work, Hall, Box

@pytest.mark.django_db
def test_specialization_number_divisible_by_5():
    s = Specialization(specialization="Test", number=11)
    with pytest.raises(ValidationError):
        s.clean()

@pytest.mark.django_db
def test_master_id_length():
    hall = Hall.objects.create(hall="H1")
    m = Master(master_id="123", first_name="A", last_name="B", password="x")
    m.save()
    m.halls.add(hall)
    with pytest.raises(ValidationError):
        m.clean()

@pytest.mark.django_db
def test_worker_id_length():
    hall = Hall.objects.create(hall="H2")
    box = Box.objects.create(number_box=1, hall=hall)
    w = Worker(worker_id="123", first_name="A", last_name="B", password="x", box=box)
    with pytest.raises(ValidationError):
        w.clean()

@pytest.mark.django_db
def test_work_id_length_and_time_length():
    hall = Hall.objects.create(hall="H3")
    box = Box.objects.create(number_box=2, hall=hall)
    m = Master.objects.create(master_id="1234567890", first_name="X", last_name="Y", password="z")
    m.halls.add(hall)
    spec = Specialization.objects.create(specialization="Spec", number=10)
    w = Work(id_work="123", time_on_work=1234567, master=m, specialization=spec)
    with pytest.raises(ValidationError):
        w.clean()
