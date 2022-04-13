from django.db import models
from users.models import CustomUser
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(
        CustomUser, null=True, blank=True, on_delete=models.CASCADE
    )


class Post(models.Model):
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    post_id = models.AutoField
    post_content = models.CharField(max_length=5000)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "{}".format(self.timestamp.__str__())


class Replie(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default="")
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "{}".format(self.timestamp.__str__())
