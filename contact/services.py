from datetime import datetime, timezone

from config.database import db


contact_collection = db["contact_messages"]


def create_contact_message(data):
    """
    Save a contact form message into MongoDB.
    """

    contact_data = {
        "full_name": data["full_name"].strip(),
        "email": data["email"].strip().lower(),
        "phone": data["phone"].strip(),
        "subject": data["subject"].strip(),
        "message": data["message"].strip(),

        "status": "unread",

        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }

    result = contact_collection.insert_one(contact_data)

    return {
        "id": str(result.inserted_id),
        "full_name": contact_data["full_name"],
        "email": contact_data["email"],
        "phone": contact_data["phone"],
        "subject": contact_data["subject"],
        "message": contact_data["message"],
        "status": contact_data["status"],
        "created_at": contact_data["created_at"].isoformat(),
    }