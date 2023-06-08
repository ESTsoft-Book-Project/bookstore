from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.urls import reverse
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
            # TODO: Does not show in templates!
            return render(request, "signup.html", {"form": SignupForm()})
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

def profile(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        update_password = request.POST["password"]
        if update_password:
            user.set_password(update_password)
        user.save()
        return redirect("users:profile")
    else:
        return render(request, "profile.html", {"user": request.user})

def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect("/")    

def signout(request):
    logout(request)
    return JsonResponse({'result': True, 'redirect': '', 'statusCode': 200})

