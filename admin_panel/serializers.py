from rest_framework import serializers


class DoctorCreateSerializer(serializers.Serializer):

    first_name = serializers.CharField(
        max_length=50
    )

    last_name = serializers.CharField(
        max_length=50
    )

    email = serializers.EmailField()

    phone = serializers.CharField(
        max_length=20
    )

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    department = serializers.CharField(
        max_length=100
    )

    specialization = serializers.CharField(
        max_length=100
    )

    experience = serializers.IntegerField(
        min_value=0
    )

    def validate_first_name(self, value):
        return value.strip()

    def validate_last_name(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip().lower()

    def validate_phone(self, value):
        return value.strip()

    def validate_department(self, value):
        return value.strip()

    def validate_specialization(self, value):
        return value.strip()


class DoctorUpdateSerializer(serializers.Serializer):

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
        required=False
    )

    department = serializers.CharField(
        max_length=100,
        required=False
    )

    specialization = serializers.CharField(
        max_length=100,
        required=False
    )

    experience = serializers.IntegerField(
        min_value=0,
        required=False
    )

    status = serializers.ChoiceField(
        choices=[
            "active",
            "inactive"
        ],
        required=False
    )

    def validate_first_name(self, value):
        return value.strip()

    def validate_last_name(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip().lower()

    def validate_phone(self, value):
        return value.strip()

    def validate_department(self, value):
        return value.strip()

    def validate_specialization(self, value):
        return value.strip()




# PATIENT SERIALIZERS
class PatientUpdateSerializer(serializers.Serializer):

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

    gender = serializers.ChoiceField(
        choices=[
            "male",
            "female",
            "other"
        ],
        required=False
    )

    date_of_birth = serializers.CharField(
        required=False,
        allow_blank=True
    )

    status = serializers.ChoiceField(
        choices=[
            "active",
            "inactive"
        ],
        required=False
    )

    def validate_first_name(self, value):
        return value.strip()

    def validate_last_name(self, value):
        return value.strip()

    def validate_email(self, value):
        return value.strip().lower()

    def validate_phone(self, value):
        return value.strip()

    def validate_date_of_birth(self, value):
        return value.strip()




# APPOINTMENT SERIALIZERS
class AppointmentCreateSerializer(serializers.Serializer):

    patient_id = serializers.CharField()

    doctor_id = serializers.CharField()

    appointment_date = serializers.DateField()

    appointment_time = serializers.TimeField()

    reason = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )

    notes = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True
    )

    status = serializers.ChoiceField(
        choices=[
            "pending",
            "confirmed",
            "completed",
            "cancelled"
        ],
        required=False,
        default="pending"
    )


class AppointmentUpdateSerializer(serializers.Serializer):

    appointment_date = serializers.DateField(
        required=False
    )

    appointment_time = serializers.TimeField(
        required=False
    )

    reason = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )

    notes = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True
    )

    status = serializers.ChoiceField(
        choices=[
            "pending",
            "confirmed",
            "completed",
            "cancelled"
        ],
        required=False
    )
    




# DEPARTMENT SERIALIZERS
class DepartmentCreateSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=100
    )

    description = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )

    status = serializers.ChoiceField(
        choices=[
            "active",
            "inactive"
        ],
        required=False,
        default="active"
    )

    def validate_name(self, value):

        return value.strip()


class DepartmentUpdateSerializer(serializers.Serializer):

    name = serializers.CharField(
        max_length=100,
        required=False
    )

    description = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True
    )

    status = serializers.ChoiceField(
        choices=[
            "active",
            "inactive"
        ],
        required=False
    )

    def validate_name(self, value):

        return value.strip()





# ADMIN USER SERIALIZERS
class AdminUserUpdateSerializer(serializers.Serializer):

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

    role = serializers.ChoiceField(
        choices=[
            "patient",
            "doctor",
            "admin"
        ],
        required=False
    )

    is_active = serializers.BooleanField(
        required=False
    )

    def validate_first_name(self, value):

        return value.strip()

    def validate_last_name(self, value):

        return value.strip()

    def validate_email(self, value):

        return value.strip().lower()

    def validate_phone(self, value):

        return value.strip()




# DASHBOARD SERIALIZER
class DashboardStatsSerializer(serializers.Serializer):

    users = serializers.DictField()

    patients = serializers.DictField()

    doctors = serializers.DictField()

    admins = serializers.DictField()

    departments = serializers.DictField()

    appointments = serializers.DictField()





# RECENT APPOINTMENTS SERIALIZER
class RecentAppointmentSerializer(
    serializers.Serializer
):

    id = serializers.CharField()

    patient_id = serializers.CharField(
        required=False,
        allow_blank=True
    )

    patient_name = serializers.CharField(
        required=False,
        allow_blank=True
    )

    patient_email = serializers.EmailField(
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

    doctor_email = serializers.EmailField(
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

    appointment_date = serializers.CharField(
        required=False,
        allow_blank=True
    )

    appointment_time = serializers.CharField(
        required=False,
        allow_blank=True
    )

    reason = serializers.CharField(
        required=False,
        allow_blank=True
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True
    )

    status = serializers.CharField(
        required=False,
        allow_blank=True
    )

    created_at = serializers.CharField(
        required=False,
        allow_blank=True
    )



# Report Serializer 
class ReportSerializer(serializers.Serializer):

    period = serializers.ChoiceField(
        choices=[
            "Today",
            "This Week",
            "This Month",
            "Last Month",
            "This Year"
        ],
        default="This Month"
    )