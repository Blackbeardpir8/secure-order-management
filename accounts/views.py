from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import RegisterSerializer, LoginSerializer
from accounts.throttles import LoginRateThrottle

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully",
                "user_id": str(user.id),  # Good practice to stringify UUIDs
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    # SECURITY: Applies the "5 requests per minute" limit we defined in settings.
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        # FIX: We must pass 'context' so the serializer can access 'request'
        # This is required for correct Django authentication signals (logging).
        serializer = LoginSerializer(data=request.data, context={"request": request})
        
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        # Generate the JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )