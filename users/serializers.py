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


