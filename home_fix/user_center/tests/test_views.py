from django.test import TestCase
from django.urls import reverse

from service.models import Order, Services
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
        self.tier = 1
        self.coin = 100
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
            tier=self.tier,
            coin=self.coin,
        )

    def test_request_view(self):
        # didn't login
        auth_test(self, "user_center:request")
        response = self.client.get(reverse("user_center:request"))
        self.assertTemplateUsed(response, "user_center/my_request_page.html")

    def test_provide_view(self):
        auth_test(self, "user_center:provide")
        response = self.client.get(reverse("user_center:provide"))
        self.assertTemplateUsed(response, "user_center/my_provide_page.html")

    def test_transaction_view(self):
        auth_test(self, "user_center:transaction")
        response = self.client.get(reverse("user_center:transaction"))
        self.assertTemplateUsed(response, "user_center/transaction.html")

    # def test_request_finish_view(self):
    #
    #     auth_test(self, "user_center:request_finish")
    #     response = self.client.get(reverse("user_center:transaction", kwargs={"order_id": 1}))

    def test_profile_view(self):
        auth_test(self, "user_center:profile")
        response = self.client.get(reverse("user_center:profile"))
        self.assertTemplateUsed(response, "user_center/profile.html")

    def test_profile_editor_view(self):
        auth_test(self, "user_center:profile_editor")
        # get request
        response = self.client.get(reverse("user_center:profile_editor"))
        self.assertTemplateUsed(response, "user_center/profile_editor.html")

        # post request
        self.client.post(
            reverse("user_center:profile_editor"), data={"gender": "female"}
        )
        user = CustomUser.objects.get(email=self.email_login)
        self.assertEqual(user.gender, "female")

    def test_provide_accept_view(self):
        service = Services.objects.create(user=self.test_user)
        order = Order.objects.create(service=service, user=self.test_user)
        response = self.client.get(
            reverse("user_center:provide_accept", kwargs={"order_id": order.id})
        )
        self.assertEquals(response.status_code, 302)

        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(
            reverse("user_center:provide_accept", kwargs={"order_id": order.id})
        )
        self.assertRedirects(response, reverse("user_center:provide"))

    def test_provide_delete_view(self):
        service = Services.objects.create(user=self.test_user)
        response = self.client.get(
            reverse("user_center:provide_delete", kwargs={"service_id": service.id})
        )
        self.assertEquals(response.status_code, 302)

        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(
            reverse("user_center:provide_delete", kwargs={"service_id": service.id})
        )
        self.assertRedirects(response, reverse("user_center:provide"))

    def test_provide_cancel_view(self):
        service = Services.objects.create(user=self.test_user)
        order = Order.objects.create(service=service, user=self.test_user)
        response = self.client.get(
            reverse("user_center:provide_cancel", kwargs={"order_id": order.id})
        )
        self.assertEquals(response.status_code, 302)

        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(
            reverse("user_center:provide_cancel", kwargs={"order_id": order.id})
        )
        self.assertRedirects(response, reverse("user_center:provide"))

    def test_notification_view(self):
        auth_test(self, "user_center:profile")
        response = self.client.get(reverse("user_center:notifications"))
        self.assertTemplateUsed(response, "user_center/notifications.html")
