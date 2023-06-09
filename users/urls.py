"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from users.views import signup, social_signup, signin, signout, profile, delete_user, updatepassword

app_name = "users"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("social/signup/", social_signup, name="social_signup"),
    path("signin/", signin, name="signin"),
    path('signout/', signout, name='signout'),
    path("signout/updatepassword/", updatepassword, name="updatepassword"),
    path("profile/", profile, name="profile"),
    path("deleteUser/", delete_user, name="delete_user"),
]
