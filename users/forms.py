from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(UserCreationForm):
    """pre-built user signup form"""

    class Meta:
        """form details"""

        model = User
        fields = ["email", "nickname", "password1", "password2"]
