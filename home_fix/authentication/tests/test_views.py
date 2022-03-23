from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_register_view_Get(self):
        response = self.client.get(reverse("authentication:register"))

        self.assertEquals(response.status_code, 200)
        # self.assertTemplateUsed(response, 'home_fix/authentication/templates/authentication/register.html')

    # def test_register_view_POST(self):
    #     response = self.client.get(reverse("authentication:register"))
    #
    #     self.assertEquals(response.status_code, 200)
