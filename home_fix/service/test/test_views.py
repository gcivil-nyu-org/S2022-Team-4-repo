from django.test import TestCase
from django.urls import reverse

from service.models import Services
from users.models import CustomUser
from utils import auth_test


class TestViews(TestCase):
    def setUp(self):
        self.email_register = "user1@gmail.com"
        self.email_login = "use2@gmail.com"
        self.first_name = "test"
        self.last_name = "test"
        self.password = "ZYHzyh1217"
        self.gender = "male"
        self.street = "nyu"
        self.state = "nyu"
        self.country = "country"
        self.zip = 10005
        self.long = 1
        self.lat = 1
        self.test_user = CustomUser.objects.create_user(
            email=self.email_login,
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            gender=self.gender,
            street=self.street,
            state=self.state,
            country=self.country,
            zip=self.zip,
            long=self.long,
            lat=self.lat,
        )

    def test_request_service_view(self):
        # didn't login
        response = self.client.get(reverse("service:request_service"))
        self.assertEquals(response.status_code, 302)

        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(reverse("service:request_service"))
        self.assertTemplateUsed(response, "service/request_services.html")

    def test_report_view(self):
        # didn't login
        service = Services.objects.create(user=self.test_user)
        response = self.client.get(
            reverse("service:report", kwargs={"service_id": service.id})
        )
        self.assertEquals(response.status_code, 302)

        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.post(
            reverse("service:report", kwargs={"service_id": service.id}),
            {"description": "xxx"},
        )
        self.assertEquals(response.status_code, 302)
