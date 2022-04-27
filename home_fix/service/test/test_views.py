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

    def test_offer_service_view(self):
        # it should redirect to index
        response = self.client.get(reverse("service:offer_service"))
        self.assertRedirects(response, reverse("users:login"))

        # it should render offer_service page
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(reverse("service:offer_service"))
        self.assertTemplateUsed(response, "service/offer_services.html")

        # it should create a service
        response = self.client.post(
            reverse("service:offer_service"),
            data={
                "category": "null",
                "description": "nul",
                "coins": 1,
                "address": "sss",
                "state": "xx",
                "country": "xxx",
                "postalcode": 10001,
                "long": 1.1,
                "lat": 1.1,
            },
        )
        self.assertRedirects(response, reverse("service:request_service"))

    def test_services_locations(self):
        auth_test(self, "service:services_locations")
        response = self.client.get(reverse("service:services_locations"))
        self.assertTemplateUsed(response, "service/services_locations.html")

    def test_service_detail_view(self):
        Services.objects.create(user=self.test_user)
        # not login
        response = self.client.get(
            reverse("service:service_detail", kwargs={"service_id": 0})
        )
        self.assertEquals(response.status_code, 302)
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(
            reverse("service:service_detail", kwargs={"service_id": 1})
        )
        self.assertTemplateUsed(response, "service/service_detail.html")

    def test_request_service_confirm_view(self):
        Services.objects.create(user=self.test_user)
        # not login
        response = self.client.get(
            reverse("service:request_service_confirm", kwargs={"service_id": 0})
        )
        self.assertEquals(response.status_code, 302)
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(
            reverse("service:request_service_confirm", kwargs={"service_id": 1})
        )
        self.assertEquals(response.status_code, 302)
