from django.contrib.auth.models import AbstractUser

# 기존 유저 모델을 상속받아 사용자 정의 모델을 생성합니다.
class CustomUser(AbstractUser):
    pass
