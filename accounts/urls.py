from django.urls import path

from .views import (
    PatientSignupView,
    LoginView,
    RefreshTokenView,
    ProfileView,
    ForgotPasswordView,
    VerifyOTPView,
    ResetPasswordView,
)


urlpatterns = [
    path(
        "signup/",
        PatientSignupView.as_view(),
        name="patient-signup"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "refresh/",
        RefreshTokenView.as_view(),
        name="token-refresh"
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),


        path(
        "forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot-password"
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
        name="verify-otp"
    ),

    path(
        "reset-password/",
        ResetPasswordView.as_view(),
        name="reset-password"
    ),
]