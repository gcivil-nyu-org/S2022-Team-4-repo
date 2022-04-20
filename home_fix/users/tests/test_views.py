from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser, Product


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
        Product.objects.create(tier=1, name="starter", price=0)
        Product.objects.create(tier=2, name="golden hammer", price=100)
        Product.objects.create(tier=3, name="loyal customer", price=150)

    def test_register_view_get(self):
        # not login
        response = self.client.get(reverse("users:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        # login

        # have location
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(reverse("users:register"))
        self.assertRedirects(response, reverse("basic:index"))
        # logout
        self.client.get(reverse("users:logout"))

        # no location
        CustomUser.objects.create_user(
            email="testregisterview@test.com",
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            gender=self.gender,
        )
        self.client.post(
            reverse("users:login"),
            data={"email": "testregisterview@test.com", "password": self.password},
        )
        response = self.client.get(reverse("users:register"))
        self.assertEqual(response.status_code, 302)

    def test_register_view_post(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "email": self.email_register,
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
                "email": self.email_register,
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

        # if user has login
        response = self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.get(reverse("users:login"))
        self.assertRedirects(response, reverse("basic:index"))

    def test_login_view_post(self):
        response = self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": "11111111"},
        )
        self.assertTemplateUsed(response, "users/login.html")

        response = self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        self.assertRedirects(response, reverse("basic:index"))

    def test_default(self):
        self.client.login(email=self.test_user.email, password=self.test_user.password)

    def test_set_location_get(self):
        response = self.client.get(reverse("users:set_location", kwargs={"user_id": 1}))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "users/set_location.html")

    def test_set_location_post_valid(self):
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        # location page
        p = reverse("users:set_location", kwargs={"user_id": 1})
        self.client.post(
            path=p,
            data={
                "country": self.country,
                "lat": self.lat,
                "long": self.long,
                "state": self.state,
                "street": self.street,
                "zip": self.zip,
            },
        )

    def test_set_location_post_invalid(self):
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        # location page
        p = reverse("users:set_location", kwargs={"user_id": 1})
        self.client.post(
            path=p,
            data={
                "country": self.country,
                "lat": self.lat,
                "long": self.long,
                "state": self.state,
                "street": self.street,
                "zip": "xxx",
            },
        )

    def test_set_location_post_url_param(self):
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        # location page
        p = reverse("users:set_location", kwargs={"user_id": 2})
        self.client.post(
            path=p,
            data={
                "country": self.country,
                "lat": self.lat,
                "long": self.long,
                "state": self.state,
                "street": self.street,
                "zip": "xxx",
            },
        )

    def test_pricing_view_get(self):
        # not login
        response = self.client.get(reverse("users:pricing"))
        self.assertRedirects(response, reverse("basic:index"))
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        # get
        response = self.client.get(reverse("users:pricing"))
        self.assertTemplateUsed(response, "users/pricing.html")

        # post wrong param
        response = self.client.post(
            reverse("users:pricing"),
            data={"tier": "asdfas"},
        )
        self.assertRedirects(response, reverse("basic:index"))
        response = self.client.post(
            reverse("users:pricing"),
            data={"tier": "4"},
        )
        self.assertRedirects(response, reverse("basic:index"))
        # post right param
        response = self.client.post(
            reverse("users:pricing"),
            data={"tier": 1},
        )
        self.assertRedirects(response, reverse("basic:index"))
        user = CustomUser.objects.get(email=self.email_login)
        assert user.tier == 1

    def test_logout_view(self):
        # login
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )

        response = self.client.get(reverse("users:logout"))
        self.assertEquals(response.status_code, 302)
        # self.assertTemplateUsed(response, "users/homepage.html")

    def test_activate(self):
        self.client.get(reverse("users:activate", kwargs={"uidb64": 1, "token": 1}))

    def test_actilink(self):
        self.client.get(reverse("users:activationlinkpage"))
