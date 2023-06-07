from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from .models import CustomUser
from django.http import HttpResponseBadRequest

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:signin')

        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                password1 = form.cleaned_data.get('password1')
                password2 = form.cleaned_data.get('password2')
                if password1 != password2:
                    form.add_error('password2', '비밀번호가 일치하지 않습니다.')
                elif len(password1) < 8:
                    form.add_error('password1', '비밀번호는 최소 8자리 이상이어야 합니다.')
                elif len(password1) < 8:
                    form.add_error('password1', '비밀번호는 최소 8자리 이상이어야 합니다.')
                elif not username.isalnum():
                    form.add_error('username', '영문과 숫자만 입력 가능합니다.')
                elif CustomUser.objects.filter(email=email).exists():
                    form.add_error('email', '중복되는 이메일입니다.')
                else:
                    user = form.save()
                    login(request, user)
                    return redirect('signin/')
        except:
            return HttpResponseBadRequest()
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        
    return render(request,'signin.html')
