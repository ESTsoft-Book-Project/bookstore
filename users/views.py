from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.urls import reverse
from .forms import SignupForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User
import json


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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({'result': True, 'redirect': '', 'statusCode': 200})
        else:
            return JsonResponse({'result': False, 'statusCode': 400})
        
    return render(request,'signin.html')

@api_view(["GET", "PATCH"])
@login_required(login_url="/users/signin/")
def profile(request):
    user = request.user
    if request.method == "GET":
        serializer = UserSerializer(user)
        return render(request, "profile.html", {"user": serializer.data})
    elif request.method == "PATCH":
        serializer = UserSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            for field in request.data.keys():
                if field != "password":
                    setattr(user, field, request.data[field])
                else:
                    user.set_password(request.data[field])
            user.save()
            return Response({"result": True, "statusCode": 200, "message": "회원 정보 수정이 완료되었습니다."})
        else:
            return Response({"result": False, "statusCode": 400, "message": "에러가 발생했습니다."})

@api_view(["DELETE"])
@login_required(login_url="/users/signin/")
def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return Response({"message": "회원 탈퇴가 완료되었습니다."})

def signout(request):
    logout(request)
    return JsonResponse({'result': True, 'redirect': '', 'statusCode': 200})
