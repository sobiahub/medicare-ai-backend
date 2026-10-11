from config.database import db
from bson import ObjectId


users_collection = db["users"]


def create_user(user_data):
    result = users_collection.insert_one(user_data)

    return users_collection.find_one({
        "_id": result.inserted_id
    })


def get_user_by_email(email):
    return users_collection.find_one({
        "email": email.lower().strip()
    })


def get_user_by_id(user_id):
    try:
        return users_collection.find_one({
            "_id": ObjectId(user_id)
        })
    except Exception:
        return None


def update_user_profile(user_id, update_data):

    try:

        result = users_collection.update_one(
            {
                "_id": ObjectId(user_id)
            },
            {
                "$set": update_data
            }
        )

        print("Matched:", result.matched_count)
        print("Modified:", result.modified_count)

        return get_user_by_id(user_id)

    except Exception as error:

        print("PROFILE UPDATE ERROR:", error)

        return None



def get_user_by_email_except_id(email, user_id):

    try:
        return users_collection.find_one({
            "email": email.lower().strip(),
            "_id": {
                "$ne": ObjectId(user_id)
            }
        })

    except Exception:
        return None




# PASSWORD RESET REPOSITORY
password_reset_collection = db["password_reset_tokens"]


def create_password_reset(reset_data):

    result = password_reset_collection.insert_one(
        reset_data
    )

    return password_reset_collection.find_one({
        "_id": result.inserted_id
    })


def get_latest_password_reset(email):

    return password_reset_collection.find_one(
        {
            "email": email.lower().strip(),
            "used": False
        },
        sort=[
            ("created_at", -1)
        ]
    )


def mark_otp_verified(
    reset_id,
    reset_token_hash,
    reset_token_expires_at
):

    from bson import ObjectId

    password_reset_collection.update_one(
        {
            "_id": ObjectId(reset_id)
        },
        {
            "$set": {
                "otp_verified": True,
                "reset_token_hash": reset_token_hash,
                "reset_token_expires_at": reset_token_expires_at
            }
        }
    )


def get_password_reset_by_token(
    reset_token_hash
):

    return password_reset_collection.find_one({
        "reset_token_hash": reset_token_hash,
        "otp_verified": True,
        "used": False
    })


def mark_password_reset_used(reset_id):

    from bson import ObjectId

    password_reset_collection.update_one(
        {
            "_id": ObjectId(reset_id)
        },
        {
            "$set": {
                "used": True
            }
        }
    )


def update_user_password(
    user_id,
    hashed_password
):

    from bson import ObjectId

    result = users_collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": {
                "password": hashed_password
            }
        }
    )

    return result.modified_count > 0