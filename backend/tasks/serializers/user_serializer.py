from rest_framework_mongoengine import serializers
from rest_framework import serializers
from tasks.models import User
from bcrypt import hashpw, gensalt

class UserSignupSerializer(serializers.DocumentSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only':True}
        }

    def create(self,validated_data):
        #hash password before saving
        raw_password = validated_data.get('password')
        if raw_password:
            hashed = hashpw(raw_password.encode('utf-8'), gensalt()).decode()
            validated_data['password'] = hashed
        return super().create(validated_data)

class UserLoginSerializer(serializers.Serializer):  
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = User.objects(email=email).first()
        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data

from rest_framework import serializers

class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

