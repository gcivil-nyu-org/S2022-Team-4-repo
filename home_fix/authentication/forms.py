from django.contrib.auth.forms import UserCreationForm, UserChangeForm, forms
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
            self.add_error("gender", "please select a gender")
            return None
        return gender

    def clean_first_name(self):
        first_name = self.data.get('first_name')
        pattern = r"[a-zA-Z]+"
        if re.match(pattern, first_name):
            return self.data.get("first_name")
        else:
            self.add_error("first_name", "please input a legal first_name")
            return None

    def clean_last_name(self):
        last_name = self.data.get('last_name')
        pattern = r"[a-zA-Z]+"
        if re.match(pattern, last_name) is None:
            self.add_error("last_name", "please select a legal last_name")
            return None
        return self.data.get("last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
