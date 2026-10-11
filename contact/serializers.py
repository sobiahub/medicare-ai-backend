from rest_framework import serializers


class ContactSerializer(serializers.Serializer):

    full_name = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False
    )

    email = serializers.EmailField(
        required=True
    )

    phone = serializers.CharField(
        max_length=30,
        required=True,
        allow_blank=False
    )

    subject = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False
    )

    message = serializers.CharField(
        max_length=2000,
        required=True,
        allow_blank=False
    )

    def validate_full_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Please enter a valid full name."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if len(value) < 7:
            raise serializers.ValidationError(
                "Please enter a valid phone number."
            )

        return value

    def validate_subject(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Please select a subject."
            )

        return value

    def validate_message(self, value):
        value = value.strip()

        if len(value) < 10:
            raise serializers.ValidationError(
                "Message must contain at least 10 characters."
            )

        return value