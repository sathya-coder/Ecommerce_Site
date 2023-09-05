from rest_framework import serializers
from ..models.User import Register


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = 'full_name','email','phone_number','company_name','address','role','created_at','password'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
