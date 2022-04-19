from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "gender")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)

        if commit:
            user.save()
        return user

    def clean_gender(self):
        gender = self.data.get("gender")
        if gender is None:
            self.add_error("gender", "Please select a gender")
            return None
        return gender

    def clean_first_name(self):
        first_name = self.data.get("first_name")
        pattern = r"[a-zA-Z]+"
        if re.match(pattern, first_name):
            return self.data.get("first_name")
        else:
            self.add_error("first_name", "Please enter First Name")
            return None

    def clean_last_name(self):
        last_name = self.data.get("last_name")
        pattern = r"[a-zA-Z]+"
        if re.match(pattern, last_name) is None:
            self.add_error("last_name", "Please enter Last Name")
            return None
        return self.data.get("last_name")


class LocationChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("country", "lat", "long", "state", "street", "zip")

    def clean_zip(self):
        zip = self.data.get("zip")
        pattern = r"(^\d{5}$)|(^\d{9}$)|(^\d{5}-\d{4}$)"
        if re.match(pattern, zip) is None:
            self.add_error("zip", "Please enter valid zip code")
            return None
        return zip


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "gender",
            # "country",
            # "lat",
            # "long",
            # "state",
            # "street",
            # "zip",
        )

    def clean_first_name(self):
        first_name = self.data.get("first_name")
        pattern = r"[a-zA-Z]+"
        if re.match(pattern, first_name):
            return self.data.get("first_name")
        else:
            self.add_error("first_name", "Please enter First Name")
            return None

    def clean_last_name(self):
        last_name = self.data.get("last_name")
        pattern = r"[a-zA-Z]+"
        if re.match(pattern, last_name) is None:
            self.add_error("last_name", "Please enter Last Name")
            return None
        return self.data.get("last_name")
