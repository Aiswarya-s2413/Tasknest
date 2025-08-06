from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from tasks.serializers import UserSignupSerializer
from tasks.models import User

class SignupView(APIView):
    def post(self, request):
        Serializer = UserSignupSerializer(data=request.data)
        if Serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects(email=email).first():
                return Response({'error': 'User already exists'},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({'message': 'User registered successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    