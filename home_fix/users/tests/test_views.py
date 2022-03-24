from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.email = "user1@gmail.com"
        self.first_name = "test"
        self.last_name = "test"
        self.password = "ZYHzyh1217"
        self.gender = "male"
        self.street = "nyu"
        self.state = "nyu"
        self.country = "country"
        self.zip = zip
        self.long = 1
        self.lat = 1

    def test_auth_view_get(self):
        response = self.client.get(reverse("users:auth"))
        self.assertEquals(response.status_code, 302)

    def test_register_view_get(self):
        response = self.client.get(reverse("users:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_register_view_post(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "gender": self.gender,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEquals(response.status_code, 302)
        response = self.client.post(
            reverse("users:register"),
            data={
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertTemplateUsed(response, "users/register.html")

    def test_login_view_get(self):
        response = self.client.get(reverse("users:login"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post(self):
        self.client.post(
            reverse("users:register"),
            data={
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "gender": self.gender,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.client.post(
            reverse("users:login"),
            data={"email": self.email, "password": self.password},
        )

    def test_set_location_get(self):
        response = self.client.get(reverse("users:set_location", kwargs={"user_id": 1}))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/set_location.html")

    def test_pricing_view_get_unauth(self):
        response = self.client.get(reverse("users:pricing"))

        self.assertEquals(response.status_code, 302)
        # self.assertTemplateUsed(response, 'authentication/pricing.html')

    def test_homepage_view(self):
        response = self.client.get(reverse("users:index"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/homepage.html")

    def test_logout_view(self):
        response = self.client.get(reverse("users:index"))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/homepage.html")

    def test_search_view(self):
        response = self.client.get(reverse("users:search"))
        self.assertEquals(response.status_code, 200)
