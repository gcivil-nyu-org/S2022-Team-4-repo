from django.shortcuts import render, redirect
from .models import Post, Replie, Profile
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from users.models import CustomUser

# Create your views here.
def forum(request):
    # profile = Profile.objects.all()
    # print("Test")
    # print(request)
    if not request.user.is_authenticated:
        return redirect("users:login")
    if request.method == "POST":
        # print("Test")
        # user = request.user
        user_id = request.user.id
        user = CustomUser.objects.get(id=user_id)
        # image = request.user.profile.image
        content = request.POST["content"]
        post = Post(user1=user, post_content=content)
        post.save()
        alert = True
        return render(request, "forum/forum.html", {"alert": alert})
    posts = Post.objects.all()
    # print(len(posts))
    return render(request, "forum/forum.html", {"posts": posts})


def discussion(request, myid):
    if not request.user.is_authenticated:
        return redirect("users:login")
    else:
        post = Post.objects.filter(id=myid).first()
        replies = Replie.objects.filter(post=post)
        if request.method == "POST":
            # user = request.user
            user_id = request.user.id
            user = CustomUser.objects.get(id=user_id)
            # image = request.user.profile.image
            desc = request.POST["desc"]
            # post_id = request.POST["post_id"]
            reply = Replie(user=user, reply_content=desc, post=post)
            reply.save()
            alert = True
            return render(request, "forum/discussion.html", {"alert": alert})
        return render(
            request, "forum/discussion.html", {"post": post, "replies": replies}
        )
