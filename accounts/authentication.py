from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from .repositories import get_user_by_id


class MongoUser:

    def __init__(self, user_data):
        self.user_data = user_data

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.user_data.get("is_active", True)

    def __getitem__(self, key):
        return self.user_data[key]

    def get(self, key, default=None):
        return self.user_data.get(key, default)

    @property
    def id(self):
        return str(self.user_data["_id"])


class MongoJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):

        header = self.get_header(request)

        if header is None:
            return None

        raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(
                raw_token
            )
        except Exception:
            raise AuthenticationFailed(
                "Invalid or expired token."
            )

        user_id = validated_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed(
                "Invalid token: user_id missing."
            )

        user = get_user_by_id(user_id)

        if not user:
            raise AuthenticationFailed(
                "User not found."
            )

        if not user.get("is_active", True):
            raise AuthenticationFailed(
                "User account is inactive."
            )

        return (
            MongoUser(user),
            validated_token
        )