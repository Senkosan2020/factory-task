from catalog.models import Worker, Box, Hall
import pytest

@pytest.mark.django_db
def test_worker_id_length():
    hall = Hall.objects.create(hall="H1")
    box = Box.objects.create(number_box=1, hall=hall)

    worker = Worker(
        worker_id="1234567890",
        first_name="Test",
        last_name="User",
        password="pass",
        box=box
    )
    worker.full_clean()
    assert worker.worker_id == "1234567890"
