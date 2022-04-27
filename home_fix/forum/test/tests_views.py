from django.test import TestCase
from django.urls import reverse

from forum.models import Post
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

    def test_post_forum(self):
        auth_test(self, "forum:Forum")
        response = self.client.post(
            reverse("forum:Forum"),
            data={"content": "sdfs"},
        )
        self.assertTemplateUsed(response, "forum/forum.html")
        response = self.client.get(
            reverse("forum:Forum"),
        )
        self.assertTemplateUsed(response, "forum/forum.html")

    def test_discussion(self):
        post = Post.objects.create(user1=self.test_user, post_content="sfd")
        response = self.client.get(
            reverse("forum:Discussions", kwargs={"myid": post.id}),
        )
        self.assertEquals(response.status_code, 302)
        self.client.post(
            reverse("users:login"),
            data={"email": self.email_login, "password": self.password},
        )
        response = self.client.post(
            reverse("forum:Discussions", kwargs={"myid": post.id}),
            data={"desc": "sdfs"},
        )
        self.assertTemplateUsed(response, "forum/discussion.html")
        response = self.client.get(
            reverse("forum:Discussions", kwargs={"myid": post.id}),
        )
        self.assertTemplateUsed(response, "forum/discussion.html")
