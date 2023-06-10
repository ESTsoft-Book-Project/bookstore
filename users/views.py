import json
from typing import cast
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
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

    if request.method == "GET":
        return render(request, "profile.html", {"user": request.user})

    elif request.method == "PATCH":
        # FIXME: #21 request.body가 json이 아니라 raw string을 리턴한다. ==> json.decoder.JSONDecodeError
        data = cast(dict, json.loads(request.body))
        print(f"patch data: {data}")

        match (data["op"]):
            case ("replace"):
                user = cast(User, request.user)
                user.nickname = data.get("nickname", user.nickname)
                user.email = data.get("email", user.email)
                update_password = data.get("password")
                if update_password:
                    user.set_password(update_password)
                    update_session_auth_hash(request, user)
                user.save()
                return JsonResponse({"message": "user profile update has completed! 🎉"})

            case ("remove"):
                request.user.delete()
                logout(request)
                return JsonResponse(
                    {"message": "You're account has succesfully deleted!"}
                )

            case (_):
                raise NotImplementedError("Other operations are not implemented")

    else:
        return HttpResponseBadRequest()
