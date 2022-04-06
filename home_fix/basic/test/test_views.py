from django.test import TestCase
from django.urls import reverse


class TestViews(TestCase):
    def test_homepage_view(self):
        response = self.client.get(reverse("basic:index"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "basic/homepage.html")
