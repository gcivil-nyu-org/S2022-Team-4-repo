from django.test import TestCase
from django.urls import reverse

from admin_system.models import Report
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
            is_staff=True,
        )

    def test_report_list_view(self):
        service = Services.objects.create(user=self.test_user)
        auth_test(self, "admin_system:report")

        # get
        response = self.client.get(reverse("admin_system:report"))
        self.assertTemplateUsed(response, "admin_system/report.html")
        # post
        report = Report.objects.create(service=service, reporter=self.test_user)
        response = self.client.post(reverse("admin_system:report"), {"report_id": 0})
        self.assertTemplateUsed(response, "admin_system/report.html")
        response = self.client.post(
            reverse("admin_system:report"), {"report_id": report.id}
        )
        self.assertTemplateUsed(response, "admin_system/report.html")

    def test_user_list_view(self):
        auth_test(self, "admin_system:user")
        response = self.client.get(reverse("admin_system:user"))
        self.assertTemplateUsed(response, "admin_system/user.html")
