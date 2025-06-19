import pytest
from catalog.models import Worker, Box, Hall

@pytest.mark.django_db
def test_worker_id_length():
    hall = Hall.objects.create(hall="A1")
    box = Box.objects.create(number_box=1, hall=hall)

    worker = Worker.objects.create(
        worker_id="1234567890",
        first_name="Test",
        last_name="User",
        password="testpass",
        box=box
    )

    assert worker.worker_id == "1234567890"
