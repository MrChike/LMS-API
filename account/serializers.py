from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  
        read_only_fields = ('id', 'created_at', 'updated_at')  




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # Check if the user exists with the provided email
        try:
            profile = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        # Check password with the stored hashed password
        if not profile.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        # If user is found and password matches, authenticate the user
        self.user = profile

        # Get the default token data (access and refresh tokens)
        data = super().validate(attrs)

        # Add the user details to the response data
        data.update({
            'email': profile.email,
            'firstName': profile.first_name,
            'lastName': profile.last_name,
            'userId': profile.user_id,  # You can include other fields you need
            'role': profile.role,  # You can include other fields you need
        })

        return data