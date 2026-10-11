from rest_framework import serializers


class PatientSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=50
    )

    last_name = serializers.CharField(
        max_length=50
    )

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        return data



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True
    )

    def validate_email(self, value):
        return value.strip().lower()



class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()



class ProfileSerializer(serializers.Serializer):

    first_name = serializers.CharField(
        max_length=50,
        required=False
    )

    last_name = serializers.CharField(
        max_length=50,
        required=False
    )

    email = serializers.EmailField(
        required=False
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )

    def validate_first_name(self, value):
        return value.strip()

    def validate_last_name(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip().lower()

    def validate_phone(self, value):
        return value.strip()




# PASSWORD RESET SERIALIZERS
class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate_email(self, value):

        return value.strip().lower()


class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(
        min_length=6,
        max_length=6
    )

    def validate_email(self, value):

        return value.strip().lower()

    def validate_otp(self, value):

        if not value.isdigit():

            raise serializers.ValidationError(
                "OTP must contain only numbers."
            )

        return value


class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()

    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True
    )

    def validate_email(self, value):

        return value.strip().lower()

    def validate(self, data):

        if data["password"] != data["confirm_password"]:

            raise serializers.ValidationError({
                "confirm_password":
                    "Passwords do not match."
            })

        return data