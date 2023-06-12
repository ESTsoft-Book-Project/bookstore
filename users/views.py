from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.urls import reverse
from .forms import SignupForm
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json


def signup(request):
    form = SignupForm()
    context = {'form': form}

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': True, 'message': '회원가입이 완료되었습니다.'}, status = 200)
            else:
                return redirect(reverse('users:signin'))
        else:
            if form.errors:
                for value in form.errors.values():
                    context['errors'] = value
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'success': False, 'message': '다시 시도해 주세요.', 'errors': value}, status = 400)
            return render(request, 'signup.html', context)

    return render(request, "signup.html", context)

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

def signout(request):
    logout(request)
    return JsonResponse({'result': True, 'redirect': '', 'statusCode': 200})
