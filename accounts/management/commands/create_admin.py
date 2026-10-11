from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from datetime import datetime, timezone

from config.database import db


users_collection = db["users"]


class Command(BaseCommand):

    help = "Create an admin user"

    def handle(self, *args, **options):

        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip().lower()
        password = input("Password: ").strip()
        phone = input("Phone: ").strip()

        # Check existing email
        existing_user = users_collection.find_one({
            "email": email
        })

        if existing_user:

            self.stdout.write(
                self.style.ERROR(
                    "A user with this email already exists."
                )
            )

            return

        admin = {

            "first_name": first_name,

            "last_name": last_name,

            "email": email,

            "password": make_password(
                password
            ),

            # Backend controlled role
            "role": "admin",

            "phone": phone,

            "is_active": True,

            "is_verified": True,

            "created_at": datetime.now(
                timezone.utc
            ),
        }

        result = users_collection.insert_one(
            admin
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin created successfully! "
                f"ID: {result.inserted_id}"
            )
        )