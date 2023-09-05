from rest_framework import serializers
from ..models.Products import *
from ..serializers.User import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('product_ids',)


class CartUpdateSerializer(serializers.Serializer):
    product_ids = serializers.CharField()
    user = serializers.CharField()

class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
    

class CheckoutSerializer(serializers.Serializer):
    user_details = RegisterSerializer()  # You might need to customize this
    products = ProductSerializer(many=True)
    payment_option = serializers.CharField(default="Cash on Delivery")



class ProductSearchSerializer(serializers.Serializer):
    search_query = serializers.CharField(max_length=100)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
        


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

class CoupunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupun
        fields = '__all__'

class UsedCoupunsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedCoupuns
        fields = '__all__'
