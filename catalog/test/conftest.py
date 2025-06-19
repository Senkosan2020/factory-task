import pytest
from catalog.models import Worker, Work
from django.contrib.auth.models import User

@pytest.fixture
def worker(db):
    return Worker.objects.create(
        first_name="Test",
        last_name="Worker",
        worker_id="1234567890"
    )

@pytest.fixture
def work(db):
    return Work.objects.create(
        code="99999",
        type="Welding",
        ready=False,
        time_on_work="1599999"
    )