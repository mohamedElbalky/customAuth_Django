from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import serializers



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number', 'password', 'password2']
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()

        return get_user_model()
    
class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(source="username", required=True,help_text="enter email or phone number", label="email/phone_number")
    password = serializers.CharField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email_or_phone', 'password']
        
    
    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active and user.is_verified:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
    
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'phone_number', 'first_name', 'last_name', "avatar"]


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['avatar']
        
    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance