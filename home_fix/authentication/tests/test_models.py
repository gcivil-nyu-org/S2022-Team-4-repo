from django.test import TestCase
from authentication.models import CustomUser


class TestModels(TestCase):
    def setUp(self):
        self.email = "user@gmail.com"
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

    def test_user_create(self):
        user = CustomUser.objects.create_user(
            email=self.email,
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
        self.assertEquals(user.email, self.email)
        user.delete()

        superuser = CustomUser.objects.create_superuser(
            email=self.email,
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
        self.assertEquals(superuser.is_superuser, True)
        superuser.delete()
