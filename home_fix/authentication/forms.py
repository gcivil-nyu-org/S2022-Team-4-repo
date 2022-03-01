from django.contrib.auth.forms import UserCreationForm, UserChangeForm, forms
from .models import CustomUser


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
        return self.data.get("gender")

    def clean_first_name(self):
        # if len(self.data.get('first_name')) < 10:
        #     raise forms.ValidationError("your username must be at least 3 characters log")
        return self.data.get("first_name")

    def clean_last_name(self):
        return self.data.get("last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
