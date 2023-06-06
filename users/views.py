from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
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

def profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        update_password = request.POST['password']
        if update_password:
            user.set_password(update_password)
        user.save()
        return redirect('users:profile')
    else:
        return render(request, 'profile.html', {'user': request.user})
    
def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('/')