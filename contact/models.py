from django.db import models

# Create your models here.
from datetime import datetime, timezone


def contact_document(
    full_name,
    email,
    phone,
    subject,
    message
):
    return {
        "full_name": full_name.strip(),
        "email": email.strip().lower(),
        "phone": phone.strip(),
        "subject": subject.strip(),
        "message": message.strip(),
        "status": "unread",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }