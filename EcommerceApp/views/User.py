from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.User import *
from ..serializers.User import *


class RegisterUser(generics.ListCreateAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

class LoginAPIView(APIView):
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = Register.objects.get(email=email)
                if (email == user.email and password == user.password):
                    user = user.email
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Bad Credentials'}, status=status.HTTP_200_OK)
            except Register.DoesNotExist:
                return Response({'message': 'Bad Credentials'}, status=status.HTTP_200_OK)

class RegisterList(generics.ListAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
