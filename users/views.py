import json
from typing import cast
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import AnonymousUser
from users.models import User
from .forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            print("DEBUG>>>>is valid!")
            form.save()
            return redirect(reverse("users:signin"))
        else:
            print("DEBUG >>> validation failed")
            print(form.errors)
            return render(request, "signup.html", {"form": form})
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def signin(request):
    if request.method == "POST":
        print(f"DEBUG >>> request.body = {request.body}")
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)

    return render(request, "signin.html")


def profile(request: HttpRequest):
    if isinstance(request.user, AnonymousUser):
        # 이렇게 하는 방법 말고 `LoginRequiredMixin`과 `UserPassesTestMixin`을 상속받는 방법이 더 좋을 것 같다.
        return HttpResponseBadRequest()

    print(f"DEBUG >>> user {request.user} has arrived!")
    user = cast(User, request.user)

    if request.method == "POST":
        user.email = request.POST["email"]
        user.nickname = request.POST["nickname"]
        update_password = request.POST["password"]
        if update_password:
            user.set_password(update_password)
            update_session_auth_hash(request, user)

        user.save()
        # FIXME: 임시로 박아넣은 render. 나중엔 JSONResponse를 리턴.
        return render(request, "profile.html", {"user": request.user})

    elif request.method == "GET":
        return render(request, "profile.html", {"user": request.user})

    else:
        return HttpResponseBadRequest()


def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect("/")
