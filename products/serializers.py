from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    
    def to_representation(self, instance):
        fields = super().to_representation(instance)
        fields["user"] = self.get_user(instance)
        fields["price"] = self.get_price(instance)
        fields["created"] = self.get_created(instance)
        fields["updated"] = self.get_updated(instance)
        return fields

    def get_user(self, obj):
        user = obj.user
        return {
            "email": user.email,
            "nickname": user.nickname
        }
    
    def get_price(self, obj):
        return "{:,.0f}원".format(obj.price) if obj.price is not None else None
    
    def get_created(self, obj):
        return obj.created.strftime("%Y-%m-%d")
    
    def get_updated(self, obj):
        return obj.updated.strftime("%Y-%m-%d")