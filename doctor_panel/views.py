from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import MongoJWTAuthentication

from .permissions import IsDoctorUser

from .services import (
    get_doctor_dashboard,
    get_doctor_appointments_data,
    get_doctor_schedule_data,
    update_doctor_schedule_data,
    get_doctor_profile_data,
    update_doctor_profile_data,

     get_doctor_patients_data,
    get_doctor_patient_data,
    get_doctor_patient_appointments_data,

    create_medical_record_data,
    get_doctor_medical_records_data,
    get_doctor_medical_record_data,
    update_medical_record_data,
    delete_medical_record_data,
)

from .serializers import (
    DoctorDashboardSerializer, 
    DoctorProfileUpdateSerializer,
    MedicalRecordCreateSerializer,
    MedicalRecordUpdateSerializer,
    MedicalRecordFilterSerializer,
)


class DoctorDashboardView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsDoctorUser
    ]

    # Get doctor dashboard
    def get(self, request):

        doctor_id = request.user["_id"]

        dashboard = get_doctor_dashboard(
            doctor_id
        )

        today_appointments = []

        for appointment in dashboard[
            "today_appointments"
        ]:

            today_appointments.append({
                "id": str(
                    appointment["_id"]
                ),
                "patient_id": str(
                    appointment.get(
                        "patient_id",
                        ""
                    )
                ),
                "patient_name": appointment.get(
                    "patient_name",
                    ""
                ),
                "patient_email": appointment.get(
                    "patient_email",
                    ""
                ),
                "appointment_date": appointment.get(
                    "appointment_date",
                    ""
                ),
                "appointment_time": appointment.get(
                    "appointment_time",
                    ""
                ),
                "reason": appointment.get(
                    "reason",
                    ""
                ),
                "status": appointment.get(
                    "status",
                    "pending"
                )
            })

        today_schedule = []

        for appointment in dashboard[
            "today_schedule"
        ]:

            today_schedule.append({
                "id": str(
                    appointment["_id"]
                ),
                "patient_id": str(
                    appointment.get(
                        "patient_id",
                        ""
                    )
                ),
                "patient_name": appointment.get(
                    "patient_name",
                    ""
                ),
                "patient_email": appointment.get(
                    "patient_email",
                    ""
                ),
                "appointment_date": appointment.get(
                    "appointment_date",
                    ""
                ),
                "appointment_time": appointment.get(
                    "appointment_time",
                    ""
                ),
                "reason": appointment.get(
                    "reason",
                    ""
                ),
                "status": appointment.get(
                    "status",
                    "pending"
                )
            })

        data = {
            "today_appointments": today_appointments,
            "today_schedule": today_schedule,
            "total_patients": dashboard[
                "total_patients"
            ],
            "pending_requests": dashboard[
                "pending_requests"
            ],
            "completed_today": dashboard[
                "completed_today"
            ],
            "recent_patients": dashboard[
                "recent_patients"
            ]
        }

        serializer = DoctorDashboardSerializer(
            data=data
        )

        serializer.is_valid(
            raise_exception=True
        )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor dashboard retrieved successfully.",
                "dashboard":
                    serializer.validated_data
            },
            status=status.HTTP_200_OK
        )



class DoctorAppointmentsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsDoctorUser
    ]

    def get(self, request):

        doctor_id = request.user["_id"]

        search = request.query_params.get(
            "search"
        )

        status_filter = request.query_params.get(
            "status"
        )

        appointment_date = request.query_params.get(
            "date"
        )

        data = get_doctor_appointments_data(
            doctor_id=doctor_id,
            search=search,
            status_filter=status_filter,
            appointment_date=appointment_date
        )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor appointments retrieved successfully.",
                "statistics":
                    data["statistics"],
                "appointments":
                    data["appointments"]
            },
            status=status.HTTP_200_OK
        )





class DoctorScheduleView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsDoctorUser
    ]

    def get(self, request):

        doctor_id = request.user["_id"]

        schedule = get_doctor_schedule_data(
            doctor_id
        )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor schedule retrieved successfully.",
                "schedule":
                    schedule
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request):

        doctor_id = request.user["_id"]

        allowed_fields = [
            "weekly_availability",
            "slot_duration",
            "consultation_type",
            "break_start",
            "break_end",
            "max_patients_per_day"
        ]

        schedule_data = {}

        for field in allowed_fields:

            if field in request.data:

                schedule_data[field] = (
                    request.data[field]
                )

        if not schedule_data:

            return Response(
                {
                    "success": False,
                    "message":
                        "No valid schedule data provided."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        update_doctor_schedule_data(
            doctor_id,
            schedule_data
        )

        schedule = get_doctor_schedule_data(
            doctor_id
        )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor schedule updated successfully.",
                "schedule":
                    schedule
            },
            status=status.HTTP_200_OK
        )




class DoctorProfileView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsDoctorUser
    ]

    def get(self, request):

        doctor_id = str(
            request.user["_id"]
        )

        doctor = get_doctor_profile_data(
            doctor_id
        )

        if not doctor:

            return Response(
                {
                    "success": False,
                    "message":
                        "Doctor profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "profile": self.serialize_profile(
                    doctor
                )
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request):

        serializer = DoctorProfileUpdateSerializer(
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        doctor_id = str(
            request.user["_id"]
        )

        updated_doctor = (
            update_doctor_profile_data(
                doctor_id,
                serializer.validated_data
            )
        )

        if not updated_doctor:

            return Response(
                {
                    "success": False,
                    "message":
                        "Doctor profile not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor profile updated successfully.",
                "profile":
                    self.serialize_profile(
                        updated_doctor
                    )
            },
            status=status.HTTP_200_OK
        )

    def serialize_profile(
        self,
        doctor
    ):

        return {

            "id":
                str(doctor["_id"]),

            "first_name":
                doctor.get(
                    "first_name",
                    ""
                ),

            "last_name":
                doctor.get(
                    "last_name",
                    ""
                ),

            "name":
                f"{doctor.get('first_name', '')} "
                f"{doctor.get('last_name', '')}".strip(),

            "email":
                doctor.get(
                    "email",
                    ""
                ),

            "phone":
                doctor.get(
                    "phone",
                    ""
                ),

            "specialization":
                doctor.get(
                    "specialization",
                    ""
                ),

            "department":
                doctor.get(
                    "department",
                    ""
                ),

            "qualification":
                doctor.get(
                    "qualification",
                    ""
                ),

            "license_number":
                doctor.get(
                    "license_number",
                    ""
                ),

            "hospital":
                doctor.get(
                    "hospital",
                    ""
                ),

            "address":
                doctor.get(
                    "address",
                    ""
                ),

            "role":
                doctor.get(
                    "role",
                    "doctor"
                ),

            "status":
                doctor.get(
                    "status",
                    "active"
                ),

            "is_active":
                doctor.get(
                    "is_active",
                    True
                ),

            "is_verified":
                doctor.get(
                    "is_verified",
                    False
                ),

            "created_at":
                doctor.get(
                    "created_at"
                ),

            "updated_at":
                doctor.get(
                    "updated_at"
                ),
        }





class DoctorPatientsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request):

        try:

            user = request.user

            # ---------------------------------------------
            # Authentication
            # ---------------------------------------------

            if not user:
                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ---------------------------------------------
            # Doctor role
            # ---------------------------------------------

            if user.get("role") != "doctor":
                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can access patients."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------------------------------------------
            # Doctor ID
            # ---------------------------------------------

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            if not doctor_id:
                return Response(
                    {
                        "success": False,
                        "message": "Doctor ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---------------------------------------------
            # Search
            # ---------------------------------------------

            search = request.query_params.get(
                "search"
            )

            if search:
                search = search.strip()

            # ---------------------------------------------
            # Get patients
            # ---------------------------------------------

            data = get_doctor_patients_data(
                doctor_id,
                search=search
            )

            return Response(
                {
                    "success": True,
                    "message": "Patients fetched successfully.",
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to fetch patients.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class DoctorPatientDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request, patient_id):

        try:

            user = request.user

            # ---------------------------------------------
            # Authentication
            # ---------------------------------------------

            if not user:
                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ---------------------------------------------
            # Doctor role
            # ---------------------------------------------

            if user.get("role") != "doctor":
                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can access patients."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------------------------------------------
            # Doctor ID
            # ---------------------------------------------

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            if not doctor_id:
                return Response(
                    {
                        "success": False,
                        "message": "Doctor ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---------------------------------------------
            # Validate patient ID
            # ---------------------------------------------

            patient_id = str(patient_id)

            # ---------------------------------------------
            # Get patient
            # ---------------------------------------------

            patient = get_doctor_patient_data(
                doctor_id,
                patient_id
            )

            if not patient:

                return Response(
                    {
                        "success": False,
                        "message": "Patient not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "success": True,
                    "message": "Patient fetched successfully.",
                    "data": patient
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to fetch patient.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




class DoctorPatientAppointmentsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request, patient_id):

        try:

            user = request.user

            # ---------------------------------------------
            # Authentication
            # ---------------------------------------------

            if not user:
                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # ---------------------------------------------
            # Doctor role
            # ---------------------------------------------

            if user.get("role") != "doctor":
                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can access patient appointments."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------------------------------------------
            # Doctor ID
            # ---------------------------------------------

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            if not doctor_id:
                return Response(
                    {
                        "success": False,
                        "message": "Doctor ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---------------------------------------------
            # Get appointments
            # ---------------------------------------------

            appointments = (
                get_doctor_patient_appointments_data(
                    doctor_id,
                    str(patient_id)
                )
            )

            return Response(
                {
                    "success": True,
                    "message": "Patient appointments fetched successfully.",
                    "data": {
                        "appointments": appointments
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to fetch patient appointments.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )






# =========================================================
# DOCTOR MEDICAL RECORDS
# =========================================================

class DoctorMedicalRecordsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    def get(self, request):

        try:

            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if user.get("role") != "doctor":

                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can access medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            if not doctor_id:

                return Response(
                    {
                        "success": False,
                        "message": "Doctor ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Filter
            record_type = request.query_params.get(
                "type"
            )

            serializer = MedicalRecordFilterSerializer(
                data={
                    "type": record_type
                }
                if record_type
                else {}
            )

            if not serializer.is_valid():

                return Response(
                    {
                        "success": False,
                        "message": "Invalid record type.",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            record_type = serializer.validated_data.get(
                "type"
            )

            records = get_doctor_medical_records_data(
                doctor_id,
                record_type=record_type
            )

            return Response(
                {
                    "success": True,
                    "message": "Medical records fetched successfully.",
                    "data": {
                        "total": len(records),
                        "records": records
                    }
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to fetch medical records.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    def post(self, request):

        try:

            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if user.get("role") != "doctor":

                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can create medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            if not doctor_id:

                return Response(
                    {
                        "success": False,
                        "message": "Doctor ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = MedicalRecordCreateSerializer(
                data=request.data
            )

            if not serializer.is_valid():

                return Response(
                    {
                        "success": False,
                        "message": "Invalid medical record data.",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            record = create_medical_record_data(
                doctor_id,
                user,
                serializer.validated_data
            )

            return Response(
                {
                    "success": True,
                    "message": "Medical record created successfully.",
                    "data": record
                },
                status=status.HTTP_201_CREATED
            )

        except ValueError as e:

            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to create medical record.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





class DoctorMedicalRecordDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    def get(self, request, record_id):

        try:

            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if user.get("role") != "doctor":

                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can access medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            record = get_doctor_medical_record_data(
                doctor_id,
                record_id
            )

            if not record:

                return Response(
                    {
                        "success": False,
                        "message": "Medical record not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "success": True,
                    "message": "Medical record fetched successfully.",
                    "data": record
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to fetch medical record.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -----------------------------------------------------
    # PATCH
    # -----------------------------------------------------

    def patch(self, request, record_id):

        try:

            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if user.get("role") != "doctor":

                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can update medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            serializer = MedicalRecordUpdateSerializer(
                data=request.data,
                partial=True
            )

            if not serializer.is_valid():

                return Response(
                    {
                        "success": False,
                        "message": "Invalid medical record data.",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            record = update_medical_record_data(
                doctor_id,
                record_id,
                serializer.validated_data
            )

            if not record:

                return Response(
                    {
                        "success": False,
                        "message": "Medical record not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "success": True,
                    "message": "Medical record updated successfully.",
                    "data": record
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to update medical record.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    def delete(self, request, record_id):

        try:

            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if user.get("role") != "doctor":

                return Response(
                    {
                        "success": False,
                        "message": "Only doctors can delete medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            doctor_id = user.get(
                "_id",
                user.get("id")
            )

            deleted = delete_medical_record_data(
                doctor_id,
                record_id
            )

            if not deleted:

                return Response(
                    {
                        "success": False,
                        "message": "Medical record not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "success": True,
                    "message": "Medical record deleted successfully."
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to delete medical record.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )