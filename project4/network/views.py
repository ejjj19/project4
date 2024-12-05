from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse

from .models import User, Post, Follow


def index(request):
    profile_user = request.user
    posts = Post.objects.all().order_by('-created_at')
    post_count = Post.objects.filter(user=profile_user).count()
    followers_count = profile_user.followers.count()  # Assuming `followers` is a related_name
    following_count = profile_user.following.count() 
    is_own_profile = request.user == profile_user
    return render(request, "network/index.html", {
        "users": profile_user,
        "posts": posts,
        "post_count": post_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_own_profile": is_own_profile
    })

def following(request):
    profile_user = request.user
    posts = Post.objects.all().order_by('-created_at')
    post_count = Post.objects.filter(user=profile_user).count()
    followers_count = profile_user.followers.count()  # Assuming `followers` is a related_name
    following_count = profile_user.following.count() 
    is_own_profile = request.user == profile_user
    return render(request, "network/index.html", {
        "users": profile_user,
        "posts": posts,
        "post_count": post_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_own_profile": is_own_profile
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        avatar = request.FILES.get("avatar")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if avatar:
                user.avatar = avatar
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def create_post(request):
    if request.method == "POST":
        create_post = request.POST["create-post"]
        username = request.user

        create = Post.objects.create(
            post = create_post,
            user = username,
        )
        create.save()

        return redirect("index")
    return render(request, "network/index.html")

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    post_count = posts.count()
    followers_count = profile_user.followers.count()  # Assuming `followers` is a related_name
    following_count = profile_user.following.count()  # Assuming `following` is a related_name
    is_own_profile = request.user == profile_user
    is_following = request.user.following.filter(id=profile_user.id).exists() if request.user.is_authenticated else False

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "posts": posts,
        "post_count": post_count,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_own_profile": is_own_profile,
        "is_following": is_following,
    })


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # Toggle following status
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    if not created:
        follow.delete()  # Unfollow
        is_following = False
    else:
        is_following = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # For AJAX requests
        return JsonResponse({'is_following': is_following})

    # Redirect for normal POST requests
    return redirect('profile', username=user_to_follow.username)