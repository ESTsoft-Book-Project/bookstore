from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from .forms import SignupForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


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

@login_required(login_url="/users/signin/")
def profile(request):
    if request.method == "POST":
        user = request.user
        user.nickname = request.POST["nickname"]
        user.email = request.POST["email"]
        update_password = request.POST["password"]
        if update_password:
            user.set_password(update_password)
            update_session_auth_hash(request, user)
        user.save()
        return JsonResponse({"message": "회원 정보 수정이 완료되었습니다."})
    else:
        return render(request, "profile.html", {"user": request.user})

@login_required(login_url="/users/signin/")
def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return JsonResponse({"message": "회원 탈퇴가 완료되었습니다."})