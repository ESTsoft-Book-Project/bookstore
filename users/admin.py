"""admin/ route에서 보여줄 정보들에 대하여 정의한다."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import SignupForm
from .models import User


class Admin(UserAdmin):
    add_form = SignupForm
    model = User
    list_display = ["email", "nickname", "is_staff", "is_active"]
    list_filter = ["email"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Nickname", {"fields": ["nickname"]}),
        ("Permissions", {"fields": ["is_staff"]}),
    ]

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["email", "nickname", "password1", "password2"]})
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, Admin)
admin.site.unregister(Group)
