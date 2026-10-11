from datetime import datetime, timezone
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import hashlib
import secrets

from datetime import timedelta
from .repositories import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_user_by_email_except_id,
    update_user_profile,
    create_password_reset,
    get_latest_password_reset,
    mark_otp_verified,
    get_password_reset_by_token,
    mark_password_reset_used,
    update_user_password,
)


def register_patient(data):
    email = data["email"].lower().strip()

    existing_user = get_user_by_email(email)

    if existing_user:
        raise ValueError(
            "An account with this email already exists."
        )

    patient = {
        "first_name": data["first_name"].strip(),
        "last_name": data["last_name"].strip(),
        "email": email,

        "password": make_password(
            data["password"]
        ),

        # IMPORTANT:
        # Role is controlled by backend.
        "role": "patient",

        "phone": data.get("phone", "").strip(),

        "is_active": True,
        "is_verified": False,

        "created_at": datetime.now(timezone.utc),
    }

    return create_user(patient)


def authenticate_user(email, password):

    user = get_user_by_email(
        email.lower().strip()
    )

    if not user:
        return None

    if not check_password(
        password,
        user["password"]
    ):
        return None

    if not user.get("is_active", True):
        return None

    return user





def generate_tokens(user):

    refresh = RefreshToken()

    refresh["user_id"] = str(user["_id"])
    refresh["email"] = user["email"]
    refresh["role"] = user["role"]

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }




def refresh_access_token(refresh_token):

    try:
        refresh = RefreshToken(refresh_token)

        user_id = refresh.get("user_id")

        if not user_id:
            return None

        user = get_user_by_id(user_id)

        if not user:
            return None

        if not user.get("is_active", True):
            return None

        access_token = refresh.access_token

        return {
            "access": str(access_token),
        }

    except TokenError:
        return None

    except Exception:
        return None




def get_profile(user_id):

    user = get_user_by_id(user_id)

    if not user:
        return None

    return user



def update_profile(user_id, data):

    update_data = {}

    if "first_name" in data:
        update_data["first_name"] = data["first_name"]

    if "last_name" in data:
        update_data["last_name"] = data["last_name"]

    if "email" in data:

        email = data["email"].lower().strip()

        existing_user = get_user_by_email_except_id(
            email,
            user_id
        )

        if existing_user:
            raise ValueError(
                "An account with this email already exists."
            )

        update_data["email"] = email

    if "phone" in data:
        update_data["phone"] = data["phone"]

    if not update_data:
        return None

    return update_user_profile(
        user_id,
        update_data
    )




# PASSWORD RESET SERVICES
def generate_otp():

    return str(
        secrets.randbelow(900000) + 100000
    )


def hash_value(value):

    return hashlib.sha256(
        value.encode()
    ).hexdigest()



def create_password_reset_request(email):

    email = email.lower().strip()

    user = get_user_by_email(email)

    # Do not expose whether the email exists
    if not user:

        return None

    otp = generate_otp()

    otp_hash = hash_value(otp)

    now = datetime.now(timezone.utc)

    reset_data = {

        "user_id": str(user["_id"]),

        "email": email,

        "otp_hash": otp_hash,

        "otp_verified": False,

        "used": False,

        "created_at": now,

        "otp_expires_at": (
            now + timedelta(minutes=10)
        )
    }

    create_password_reset(
        reset_data
    )

    # Temporary development solution.
    # Later we will send this OTP through email.
    print(
        f"\nPASSWORD RESET OTP"
        f"\nEmail: {email}"
        f"\nOTP: {otp}\n"
    )

    return True



def verify_password_reset_otp(
    email,
    otp
):

    email = email.lower().strip()

    reset_request = get_latest_password_reset(
        email
    )

    if not reset_request:

        return None, "Invalid or expired OTP."

    now = datetime.now(timezone.utc)

    otp_expires_at = reset_request[
        "otp_expires_at"
    ]

    # MongoDB returns naive UTC datetime
    if otp_expires_at.tzinfo is None:

        otp_expires_at = otp_expires_at.replace(
            tzinfo=timezone.utc
        )

    if now > otp_expires_at:

        return None, "OTP has expired."

    otp_hash = hash_value(otp)

    if otp_hash != reset_request["otp_hash"]:

        return None, "Invalid OTP."

    # Generate temporary reset token
    reset_token = secrets.token_urlsafe(32)

    reset_token_hash = hash_value(
        reset_token
    )

    reset_token_expires_at = (
        now + timedelta(minutes=15)
    )

    mark_otp_verified(
        str(reset_request["_id"]),
        reset_token_hash,
        reset_token_expires_at
    )

    return reset_token, None



def reset_user_password(
    email,
    reset_token,
    new_password
):

    email = email.lower().strip()

    token_hash = hash_value(
        reset_token
    )

    reset_request = get_password_reset_by_token(
        token_hash
    )

    if not reset_request:

        return False, "Invalid reset token."

    # Make sure token belongs to same email
    if reset_request["email"] != email:

        return False, "Invalid reset token."

    now = datetime.now(timezone.utc)

    reset_token_expires_at = (
        reset_request["reset_token_expires_at"]
    )

    # MongoDB may return a naive UTC datetime
    if reset_token_expires_at.tzinfo is None:

        reset_token_expires_at = (
            reset_token_expires_at.replace(
                tzinfo=timezone.utc
            )
        )

    if now > reset_token_expires_at:

        return False, "Reset token has expired."

    user = get_user_by_email(
        email
    )

    if not user:

        return False, "Unable to reset password."

    hashed_password = make_password(
        new_password
    )

    updated = update_user_password(
        str(user["_id"]),
        hashed_password
    )

    if not updated:

        return False, "Unable to update password."

    # Token can no longer be used
    mark_password_reset_used(
        str(reset_request["_id"])
    )

    return True, None