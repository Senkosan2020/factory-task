import pytest
from catalog.models import Work, Master, Specialization
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_protected_view_redirects_anonymous(client):
    # Підготовка залежних об'єктів
    spec = Specialization.objects.create(specialization="Test", number=10)
    master = Master.objects.create(master_id="1234567890", first_name="M", last_name="M", password="1234")
    work = Work.objects.create(
        id_work="W123456",
        time_on_work=1234567,
        ready=False,
        master=master,
        specialization=spec,
    )

    url = reverse("work_detail", kwargs={"pk": work.pk})
    response = client.get(url)
    assert response.status_code == 302 or response.status_code == 403
