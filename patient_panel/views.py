from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.authentication import MongoJWTAuthentication


from .services import (
    get_patient_dashboard,
    get_patient_appointments_data,
    get_patient_appointment_details,
    cancel_appointment,
    ALLOWED_STATUS_FILTERS,
    get_patient_medical_records_data,
    get_patient_medical_record_data,
    get_medical_record_download_data,
)

from .serializers import MedicalRecordFilterSerializer

class PatientDashboardView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request):

        try:

            # Get authenticated user
            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Get patient ID

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:

                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

           # Make sure user is patient

            role = user.get("role")

            if role != "patient":

                return Response(
                    {
                        "success": False,
                        "message": "Only patients can access this dashboard."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Get dashboard data

            data = get_patient_dashboard(
                patient_id
            )

            if not data:

                return Response(
                    {
                        "success": False,
                        "message": "Patient not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # Success response

            return Response(
                {
                    "success": True,
                    "message": "Patient dashboard data fetched successfully.",
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to fetch patient dashboard.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







class PatientAppointmentsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request):

        try:

            # Authenticated user

            user = request.user

            if not user:

                return Response(
                    {
                        "success": False,
                        "message": "Authentication required."
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Check patient role

            if user.get("role") != "patient":

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Only patients can access "
                            "their appointments."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # Get patient ID

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:

                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Status filter

            status_filter = request.query_params.get(
                "status"
            )

            if status_filter:

                status_filter = status_filter.lower()

                if status_filter not in ALLOWED_STATUS_FILTERS:

                    return Response(
                        {
                            "success": False,
                            "message": (
                                "Invalid appointment status."
                            ),
                            "allowed_statuses": [
                                "upcoming",
                                "pending",
                                "confirmed",
                                "completed",
                                "cancelled"
                            ]
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Get appointments

            data = get_patient_appointments_data(
                patient_id,
                status_filter
            )

            # Response
            return Response(
                {
                    "success": True,
                    "message": (
                        "Appointments fetched successfully."
                    ),
                    "data": data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Unable to fetch appointments."
                    ),
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PatientAppointmentDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(
        self,
        request,
        appointment_id
    ):

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

            if user.get("role") != "patient":

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Only patients can access "
                            "appointment details."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:

                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            appointment = get_patient_appointment_details(
                patient_id,
                appointment_id
            )

            if not appointment:

                return Response(
                    {
                        "success": False,
                        "message": "Appointment not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "success": True,
                    "message": (
                        "Appointment fetched successfully."
                    ),
                    "data": appointment
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Unable to fetch appointment."
                    ),
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CancelPatientAppointmentView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def patch(
        self,
        request,
        appointment_id
    ):

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

            if user.get("role") != "patient":

                return Response(
                    {
                        "success": False,
                        "message": (
                            "Only patients can cancel "
                            "their appointments."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:

                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            result = cancel_appointment(
                patient_id,
                appointment_id
            )

            if not result["success"]:

                return Response(
                    result,
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                result,
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Unable to cancel appointment."
                    ),
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





# =========================================================
# MEDICAL RECORDS LIST
# =========================================================

class PatientMedicalRecordsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request):

        try:

            user = request.user

            # ---------------------------------------------
            # Check authentication
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
            # Check patient role
            # ---------------------------------------------

            if user.get("role") != "patient":
                return Response(
                    {
                        "success": False,
                        "message": "Only patients can access medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------------------------------------------
            # Get patient ID
            # ---------------------------------------------

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:
                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---------------------------------------------
            # Get filter
            # ---------------------------------------------

            record_type = request.query_params.get("type")

            # ---------------------------------------------
            # Validate filter
            # ---------------------------------------------

            filter_serializer = MedicalRecordFilterSerializer(
                data={
                    "type": record_type
                }
                if record_type
                else {}
            )

            if not filter_serializer.is_valid():

                return Response(
                    {
                        "success": False,
                        "message": "Invalid record type.",
                        "errors": filter_serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            record_type = filter_serializer.validated_data.get(
                "type"
            )

            # ---------------------------------------------
            # Get records
            # ---------------------------------------------

            data = get_patient_medical_records_data(
                patient_id,
                record_type=record_type
            )

            return Response(
                {
                    "success": True,
                    "message": "Medical records fetched successfully.",
                    "data": data
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


# =========================================================
# SINGLE MEDICAL RECORD
# =========================================================

class PatientMedicalRecordDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request, record_id):

        try:

            user = request.user

            # ---------------------------------------------
            # Check authentication
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
            # Check patient role
            # ---------------------------------------------

            if user.get("role") != "patient":
                return Response(
                    {
                        "success": False,
                        "message": "Only patients can access medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------------------------------------------
            # Get patient ID
            # ---------------------------------------------

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:
                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---------------------------------------------
            # Get record
            # ---------------------------------------------

            record = get_patient_medical_record_data(
                patient_id,
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


# =========================================================
# DOWNLOAD MEDICAL RECORD
# =========================================================

class PatientMedicalRecordDownloadView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    def get(self, request, record_id):

        try:

            user = request.user

            # ---------------------------------------------
            # Check authentication
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
            # Check patient role
            # ---------------------------------------------

            if user.get("role") != "patient":
                return Response(
                    {
                        "success": False,
                        "message": "Only patients can download medical records."
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            # ---------------------------------------------
            # Get patient ID
            # ---------------------------------------------

            patient_id = user.get(
                "_id",
                user.get("id")
            )

            if not patient_id:
                return Response(
                    {
                        "success": False,
                        "message": "Patient ID not found."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ---------------------------------------------
            # Get file
            # ---------------------------------------------

            file_data = get_medical_record_download_data(
                patient_id,
                record_id
            )

            if not file_data:

                return Response(
                    {
                        "success": False,
                        "message": "Medical record not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # ---------------------------------------------
            # Check file
            # ---------------------------------------------

            if not file_data.get("file_url"):

                return Response(
                    {
                        "success": False,
                        "message": "No file is available for this medical record."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                    "success": True,
                    "message": "Medical record file found.",
                    "data": file_data
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:

            return Response(
                {
                    "success": False,
                    "message": "Unable to download medical record.",
                    "error": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )