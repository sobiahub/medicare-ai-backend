from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .authentication import MongoJWTAuthentication

from .services import (
    register_patient,
    authenticate_user,
    generate_tokens,
    refresh_access_token,
    update_profile,
    create_password_reset_request,
    verify_password_reset_otp,
    reset_user_password,
)

from .serializers import (
    PatientSignupSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    ProfileSerializer,
    ForgotPasswordSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
)

class PatientSignupView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = PatientSignupSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            patient = register_patient(
                serializer.validated_data
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Patient account created successfully.",
                "user": {
                    "id": str(patient["_id"]),
                    "first_name": patient["first_name"],
                    "last_name": patient["last_name"],
                    "email": patient["email"],
                    "role": patient["role"],
                    "phone": patient["phone"],
                },
            },
            status=status.HTTP_201_CREATED
        )



class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate_user(
            email,
            password
        )

        if not user:
            return Response(
                {
                    "success": False,
                    "message": "Invalid email or password."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = generate_tokens(user)

        return Response(
            {
                "success": True,
                "message": "Login successful.",

                "user": {
                    "id": str(user["_id"]),
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                    "role": user["role"],
                    "phone": user.get("phone", ""),
                },

                "tokens": tokens,
            },
            status=status.HTTP_200_OK
        )



class RefreshTokenView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RefreshTokenSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        refresh_token = serializer.validated_data["refresh"]

        tokens = refresh_access_token(
            refresh_token
        )

        if not tokens:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "success": True,
                "message": "Access token refreshed successfully.",
                "tokens": tokens,
            },
            status=status.HTTP_200_OK
        )




class ProfileView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request):

        user = request.user

        return Response(
            {
                "success": True,
                "user": {
                    "id": str(user["_id"]),
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                    "email": user.get("email", ""),
                    "role": user.get("role", ""),
                    "phone": user.get("phone", ""),
                }
            },
            status=status.HTTP_200_OK
        )

    def put(self, request):

        return self._update_profile(
            request,
            partial=False
        )

    def patch(self, request):

        return self._update_profile(
            request,
            partial=True
        )

    def _update_profile(self, request, partial=False):

        serializer = ProfileSerializer(
            data=request.data,
            partial=partial
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_user = update_profile(
            str(request.user["_id"]),
            serializer.validated_data
        )

        if not updated_user:
            return Response(
                {
                    "success": False,
                    "message": "Unable to update profile."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message": "Profile updated successfully.",
                "user": {
                    "id": str(updated_user["_id"]),
                    "first_name": updated_user.get(
                        "first_name", ""
                    ),
                    "last_name": updated_user.get(
                        "last_name", ""
                    ),
                    "email": updated_user.get(
                        "email", ""
                    ),
                    "role": updated_user.get(
                        "role", ""
                    ),
                    "phone": updated_user.get(
                        "phone", ""
                    ),
                }
            },
            status=status.HTTP_200_OK
        )



class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        create_password_reset_request(
            email
        )

        return Response(
            {
                "success": True,
                "message":
                    "If an account exists with this email, "
                    "a verification code has been sent."
            },
            status=status.HTTP_200_OK
        )





class ForgotPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        create_password_reset_request(
            email
        )

        return Response(
            {
                "success": True,
                "message":
                    "If an account exists with this email, "
                    "a verification code has been sent."
            },
            status=status.HTTP_200_OK
        )




class VerifyOTPView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = VerifyOTPSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        otp = serializer.validated_data[
            "otp"
        ]

        reset_token, error = (
            verify_password_reset_otp(
                email,
                otp
            )
        )

        if error:

            return Response(
                {
                    "success": False,
                    "message": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "OTP verified successfully.",
                "reset_token": reset_token
            },
            status=status.HTTP_200_OK
        )



class ResetPasswordView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = ResetPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data[
            "email"
        ]

        token = serializer.validated_data[
            "token"
        ]

        password = serializer.validated_data[
            "password"
        ]

        success, error = (
            reset_user_password(
                email,
                token,
                password
            )
        )

        if not success:

            return Response(
                {
                    "success": False,
                    "message": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Password reset successfully."
            },
            status=status.HTTP_200_OK
        )