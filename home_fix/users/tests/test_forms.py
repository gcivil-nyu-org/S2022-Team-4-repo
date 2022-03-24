from django.test import TestCase

from users.forms import CustomUserCreationForm, LocationForm


class TestForms(TestCase):
    def test_custom_user_create_form(self):
        form = CustomUserCreationForm(
            data={
                "email": "test",
                "first_name": "first_name",
                "last_name": "last_name",
                "gender": "male",
            }
        )
        if form.is_valid():
            user = form.save(commit=True)
            user.save()
            self.assertEquals(user.email, "test")
        form2 = form = CustomUserCreationForm(
            data={"email": "test", "first_name": "12312", "last_name": "23423"}
        )
        self.assertEquals(form2.is_valid(), False)

    def test_location_form(self):
        form = LocationForm(
            data={
                "country": "country",
                "lat": 111,
                "long": 111,
                "state": "state",
                "street": "street",
                "zip": "xx",
            }
        )
        self.assertEquals(form.is_valid(), False)
        form = LocationForm(
            data={
                "country": "country",
                "lat": 111,
                "long": 111,
                "state": "state",
                "street": "street",
                "zip": "10005",
            }
        )
        self.assertEquals(form.is_valid(), True)
