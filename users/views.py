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
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': '회원가입이 완료되었습니다.', 'redirect': reverse('users:signin')})        
        else:
            errors = serializer.errors
            return Response({'success': False, 'message': '다시 시도해 주세요.', 'errors': errors},)
    
    elif request.method == 'GET':
        return render(request, 'signup.html')
       
@api_view(['POST', 'GET'])
def signin(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return Response({'result': True, 'redirect': ''})
        else:
            return Response({'result': False})
    
    elif request.method == 'GET':
        return render(request, 'signin.html')


@login_required(login_url="/users/signin/")
def profile(request):
    if request.method == "PATCH":
        user = request.user
        user.email = json.loads(request.body).get("email", user.email)
        user.nickname = json.loads(request.body).get("nickname", user.nickname)
        update_password = json.loads(request.body).get("password")
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


@api_view(["POST"])
def signout(request):
    if request.method == 'POST':
        logout(request)
        return Response({'result': True, 'redirect': ''})
    else:
        return Response({'result': False, 'message': '잘못된 요청입니다.'})
