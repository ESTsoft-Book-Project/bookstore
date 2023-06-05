from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """ref: https://dontrepeatyourself.org/post/django-custom-user-model-extending-abstractuser/"""

    def create_user(self, email, nickname=None, password=None):
        """Create and save a User with the given email and password"""
        if not email:
            raise ValueError("The Email field must be set!!! 💀")

        user = self.model(email=self.normalize_email(email), nickname=nickname)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, nickname=None, password=None):
        """`./manage.py createsuperuser` command will call this"""
        user = self.create_user(email, nickname=nickname, password=password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model
    ref: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#a-full-example
    """

    # attributes
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # custom user manager
    objects = UserManager()

    # email field will be unique
    USERNAME_FIELD = "email"
    # required on `createsuperuser`
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self) -> str:
        return f"{str(self.nickname)}({self.email})"

    def has_perm(self, _perm, _obj=None):
        """Does the user have a specific permission? ==> Yes, always"""
        return True

    def has_module_perms(self, _app_label):
        """Does the user have permissions to view the app `app_label`? ==> Yes, always"""
        return True
