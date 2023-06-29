from rest_framework import serializers
from .models import User
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'nickname', 'password1', 'password2']
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        password2 = validated_data.pop("password2")
        if password1 != password2:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        user = User.objects.create_user(**validated_data, password=password1)
        return user

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            raise serializers.ValidationError('이메일과 비밀번호를 모두 입력해주세요.')

        # 비밀번호 유효성 검사를 수행합니다.
        try:
            password_validation.validate_password(password)
        except serializers.ValidationError as error:
            raise serializers.ValidationError({'password': error.messages})

        return data


class ProfileSerializer(serializers.ModelSerializer):
    """password는 확인하는 용도로 사용, email, nickname을 수정하는데 사용.
    참고: 초기값이 마치 placeholder처럼 지정되어있어야 한다."""
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(max_length=150)
    nickname = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "nickname", "password"]

    def update(self, instance: User, validated_data):
        if not instance.check_password(validated_data.get("password")):
            raise serializers.ValidationError({"password": "사용자 비밀번호가 틀렸습니다."})
        instance.email = validated_data.get("email")
        instance.nickname = validated_data.get("nickname")
        instance.save()
        return instance


class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["password", "password1", "password2"]

    def validate(self, attrs):
        password_validation.validate_password(attrs["password1"])
            # raise serializers.ValidationError({"password1": "새 비밀번호가 조건을 만족하지 않습니다."})
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password1": "새 비밀번호가 서로 일치하지 않습니다."})
        if attrs["password"] == attrs["password1"]:
            raise serializers.ValidationError({"password1": "비밀번호는 이전에 사용하던 것을 사용할 수 없습니다."})
        return attrs

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data.get("password")):
            raise serializers.ValidationError({"password": "사용자 비밀번호가 틀렸습니다."})
        instance.set_password(validated_data.get("password2"))
        instance.save()
        return instance
