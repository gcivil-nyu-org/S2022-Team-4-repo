from django.contrib import admin

# Register your models here.
from .models import Post, Replie, Profile

admin.site.register(Post)
admin.site.register(Replie)
admin.site.register(Profile)
