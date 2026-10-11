from rest_framework import serializers


class DoctorDashboardAppointmentSerializer(
    serializers.Serializer
):

    id = serializers.CharField()
    patient_id = serializers.CharField(
        allow_blank=True,
        required=False
    )
    patient_name = serializers.CharField(
        allow_blank=True,
        required=False
    )
    patient_email = serializers.CharField(
        allow_blank=True,
        required=False
    )
    appointment_date = serializers.CharField(
        allow_blank=True,
        required=False
    )
    appointment_time = serializers.CharField(
        allow_blank=True,
        required=False
    )
    reason = serializers.CharField(
        allow_blank=True,
        required=False
    )
    status = serializers.CharField(
        allow_blank=True,
        required=False
    )


class DoctorRecentPatientSerializer(
    serializers.Serializer
):

    patient_id = serializers.CharField()
    patient_name = serializers.CharField(
        allow_blank=True,
        required=False
    )
    patient_email = serializers.CharField(
        allow_blank=True,
        required=False
    )
    appointment_date = serializers.CharField(
        allow_blank=True,
        required=False
    )
    appointment_time = serializers.CharField(
        allow_blank=True,
        required=False
    )
    status = serializers.CharField(
        allow_blank=True,
        required=False
    )


class DoctorDashboardSerializer(
    serializers.Serializer
):

    today_appointments = DoctorDashboardAppointmentSerializer(
        many=True
    )

    today_schedule = DoctorDashboardAppointmentSerializer(
        many=True
    )

    total_patients = serializers.IntegerField()

    pending_requests = serializers.IntegerField()

    completed_today = serializers.IntegerField()

    recent_patients = DoctorRecentPatientSerializer(
        many=True
    )





class DoctorProfileUpdateSerializer(serializers.Serializer):

    first_name = serializers.CharField(
        required=False,
        max_length=100
    )

    last_name = serializers.CharField(
        required=False,
        max_length=100
    )

    phone = serializers.CharField(
        required=False,
        max_length=30
    )

    specialization = serializers.CharField(
        required=False,
        max_length=150
    )

    department = serializers.CharField(
        required=False,
        max_length=150
    )

    qualification = serializers.CharField(
        required=False,
        max_length=150
    )

    license_number = serializers.CharField(
        required=False,
        max_length=100
    )

    hospital = serializers.CharField(
        required=False,
        max_length=200
    )

    address = serializers.CharField(
        required=False,
        max_length=300
    )





class DoctorPatientSerializer(serializers.Serializer):

    id = serializers.CharField()

    first_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    last_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True
    )

    phone = serializers.CharField(
        required=False,
        allow_blank=True
    )

    gender = serializers.CharField(
        required=False,
        allow_blank=True
    )

    is_active = serializers.BooleanField(
        required=False
    )

    is_verified = serializers.BooleanField(
        required=False
    )

    created_at = serializers.CharField(
        required=False,
        allow_null=True
    )

    updated_at = serializers.CharField(
        required=False,
        allow_null=True
    )






# CREATE MEDICAL RECORD
# =========================================================

class MedicalRecordCreateSerializer(
    serializers.Serializer
):

    patient_id = serializers.CharField()

    type = serializers.ChoiceField(
        choices=[
            "consultation",
            "lab_report",
            "prescription"
        ]
    )

    title = serializers.CharField(
        max_length=200
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    department = serializers.CharField(
        required=False,
        allow_blank=True
    )

    specialization = serializers.CharField(
        required=False,
        allow_blank=True
    )

    date = serializers.DateField()

    status = serializers.CharField(
        required=False,
        default="available"
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )

    file_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    file_url = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )


# =========================================================
# UPDATE MEDICAL RECORD
# =========================================================

class MedicalRecordUpdateSerializer(
    serializers.Serializer
):

    type = serializers.ChoiceField(
        choices=[
            "consultation",
            "lab_report",
            "prescription"
        ],
        required=False
    )

    title = serializers.CharField(
        max_length=200,
        required=False
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    department = serializers.CharField(
        required=False,
        allow_blank=True
    )

    specialization = serializers.CharField(
        required=False,
        allow_blank=True
    )

    date = serializers.DateField(
        required=False
    )

    status = serializers.CharField(
        required=False
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )

    file_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    file_url = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )


# =========================================================
# FILTER
# =========================================================

class MedicalRecordFilterSerializer(
    serializers.Serializer
):

    type = serializers.ChoiceField(
        choices=[
            "consultation",
            "lab_report",
            "prescription"
        ],
        required=False
    )