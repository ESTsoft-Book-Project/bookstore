from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["email", "nickname", "password1", "password2"]
    
    def create(self, validated_data):
        password1 = validated_data.pop("password1")
        password2 = validated_data.pop("password2")
        if password1 != password2:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        user = User.objects.create_user(**validated_data, password=password1)
        return user
    