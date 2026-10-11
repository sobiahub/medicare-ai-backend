from rest_framework import serializers


class PatientDashboardSerializer(serializers.Serializer):

    patient = serializers.DictField()

    doctor = serializers.DictField(
        allow_null=True
    )

    quick_actions = serializers.DictField()

    recent_appointments = serializers.ListField()

    health_summary = serializers.DictField()

    appointment_reminder = serializers.DictField(
        allow_null=True
    )





class PatientAppointmentSerializer(
    serializers.Serializer
):

    id = serializers.CharField()

    patient_id = serializers.CharField()

    patient_name = serializers.CharField()

    patient_email = serializers.EmailField()

    doctor_id = serializers.CharField()

    doctor_name = serializers.CharField()

    doctor_email = serializers.EmailField()

    department = serializers.CharField()

    specialization = serializers.CharField()

    appointment_date = serializers.CharField()

    appointment_time = serializers.CharField()

    reason = serializers.CharField(
        allow_blank=True
    )

    notes = serializers.CharField(
        allow_blank=True
    )

    status = serializers.CharField()


class AppointmentSummarySerializer(
    serializers.Serializer
):

    total = serializers.IntegerField()

    upcoming = serializers.IntegerField()

    completed = serializers.IntegerField()

    cancelled = serializers.IntegerField()






class MedicalRecordSerializer(serializers.Serializer):
    id = serializers.CharField()
    patient_id = serializers.CharField(required=False, allow_blank=True)

    title = serializers.CharField()
    type = serializers.CharField()

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    doctor_id = serializers.CharField(
        required=False,
        allow_blank=True
    )

    doctor_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    doctor_email = serializers.CharField(
        required=False,
        allow_blank=True
    )

    specialization = serializers.CharField(
        required=False,
        allow_blank=True
    )

    department = serializers.CharField(
        required=False,
        allow_blank=True
    )

    date = serializers.CharField()

    status = serializers.CharField(
        required=False,
        allow_blank=True
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

    created_at = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    updated_at = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )


class MedicalRecordFilterSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[
            "consultation",
            "lab_report",
            "prescription"
        ],
        required=False
    )