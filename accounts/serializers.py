from django.contrib.auth import authenticate
from rest_framework import serializers
#from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    User registration serializer.

    # Point 8: Input validation
    """

    password = serializers.CharField(write_only=True, min_length=8)
    #password = serializers.CharField(write_only=True, required=True, validators=[validate_password]  # Enforces Django's strict password rules) but not using for my ease.

    class Meta:
        model = User
        fields = ("id", "email", "password", "role")
        # SECURITY: Prevents users from making themselves Admin during signup
        read_only_fields = ("id", "role")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Login serializer using email + password.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # We pass the request context to authenticate() for potential logging/signal handling
        user = authenticate(
            email=attrs.get("email"),
            password=attrs.get("password"),
        )

        if not user:
            # Point 9: Secure error message
            # Never say "User not found" or "Wrong password". 
            # It helps hackers guess valid emails.
            raise serializers.ValidationError("Invalid login credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account is disabled")

        attrs["user"] = user
        return attrs
