from rest_framework_mongoengine import serializers
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