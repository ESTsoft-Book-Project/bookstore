from django.forms import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PasswordSerializer, ProfileSerializer, UserSerializer, SignInSerializer
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
                return Response({'message': 'Login successful', 'redirect': '/', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK )
            else:
                return Response({'message': 'Invalid username or password'})
        else: 
            return Response({'message': serializer.errors['password']})
    return render(request, 'signin.html')
    

@api_view(['GET', 'PATCH'])
@login_required
def profile(request):
    user = request.user
    if request.method == 'PATCH':
        serializer = ProfileSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            logout(request)
            redirect_url = reverse('users:signin')
            return Response({"result": True, "statusCode": 200, "message": "회원 정보 수정이 완료되었습니다.", "redirect_url": redirect_url})
    serializer = ProfileSerializer(user)
    return render(request, "profile.html", {"user": serializer.data})


@login_required
@api_view(["GET", "PATCH"])
def updatepassword(request):
    if request.method == "PATCH":
        user = request.user
        serializer = PasswordSerializer(instance=user, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

        except ValidationError:
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

        logout(request)
        return Response({
            "message": "성공적으로 비밀번호 수정이 완료되었습니다.",
            "redirect_url": reverse("users:signin")
        }, status=status.HTTP_200_OK)

    return render(request, "updatepassword.html")


@api_view(["DELETE"])
@login_required
def delete_user(request):
    if request.method == "DELETE":
        user = request.user
        user.delete()
        logout(request)
        return Response({"message": "회원 탈퇴가 완료되었습니다."})
    else:
        return Response({"result": False})

@api_view(["POST"])
@login_required
def signout(request):
    logout(request)
    return JsonResponse(
        {"statusCode": 200,
         "message": "Succesfully Logged Out", 
         "redirect_url": reverse("users:signin")})
