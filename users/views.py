from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, SignInSerializer
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
@api_view(['POST', 'GET'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, 'message': '회원가입이 완료되었습니다.', 'redirect': '/users/signin/'})
        else:
            return Response({'success': False, 'message': '회원가입에 실패했습니다.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    return render(request, 'signup.html')
    

@csrf_exempt
@api_view(['POST', 'GET'])
def signin(request):
    serializer = SignInSerializer(data=request.data)
    if request.method == 'POST':       
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful', 'redirect': '/'}, status=status.HTTP_200_OK )
            else:
                return Response({'message': 'Invalid username or password'})
        else: 
            return Response(serializer.errors)
    return render(request, 'signin.html')
    

@api_view(['GET', 'PATCH'])
@login_required(login_url="/users/signin/")
def profile(request):
    user = request.user
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            for field in request.data.keys():
                if field != "password":
                    setattr(user, field, request.data[field])
                else:
                    user.set_password(request.data[field])
            user.save()
            logout(request)
            redirect_url = reverse('users:signin')
            return Response({"result": True, "statusCode": 200, "message": "회원 정보 수정이 완료되었습니다.", "redirect_url": redirect_url})
    elif request.method == "GET":
        serializer = UserSerializer(user)
        return render(request, "profile.html", {"user": serializer.data})
    else:
        return Response({"result": False, "statusCode": 400, "message": "에러가 발생했습니다."})

@api_view(["DELETE"])
@login_required(login_url="/users/signin/")
def delete_user(request):
    if request.method == "DELETE":
        user = request.user
        user.delete()
        logout(request)
        return Response({"message": "회원 탈퇴가 완료되었습니다."})
    else:
        return Response({"result": False})

@api_view(["POST"])
@login_required()
def signout(request):
    logout(request)
    return JsonResponse(
        {"statusCode": 200,
         "message": "Succesfully Logged Out", 
         "redirect_url": reverse("users:signin")})
