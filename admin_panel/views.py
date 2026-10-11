from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.authentication import MongoJWTAuthentication

from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated



from .serializers import (
    DoctorCreateSerializer,
    DoctorUpdateSerializer,
    PatientUpdateSerializer,
    AppointmentCreateSerializer,
    AppointmentUpdateSerializer,
    DepartmentCreateSerializer,
    DepartmentUpdateSerializer,
    AdminUserUpdateSerializer,
    DashboardStatsSerializer,
    RecentAppointmentSerializer,
    ReportSerializer
)

from .services import (
    create_new_doctor,
    get_doctors,
    get_doctor,
    update_existing_doctor,
    remove_doctor,

    get_patients,
    get_patient,
    update_existing_patient,
    remove_patient,

    create_new_appointment,
    get_appointments,
    get_appointment,
    update_existing_appointment,
    remove_appointment,

    create_new_department,
    get_departments,
    get_department,
    update_existing_department,
    remove_department,

    get_users,
    get_user,
    update_existing_user,
    remove_user,

    get_admin_dashboard_statistics,
    get_admin_recent_appointments,

    generate_report
)


class DoctorListCreateView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET ALL DOCTORS
    def get(self, request):

        doctors = get_doctors()

        doctor_list = []

        for doctor in doctors:

            doctor_list.append({

                "id": str(
                    doctor["_id"]
                ),

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

                "department":
                    doctor.get(
                        "department",
                        ""
                    ),

                "specialization":
                    doctor.get(
                        "specialization",
                        ""
                    ),

                "experience":
                    doctor.get(
                        "experience",
                        0
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
            })

        return Response(
            {
                "success": True,
                "count": len(doctor_list),
                "doctors": doctor_list,
            },
            status=status.HTTP_200_OK
        )

    # CREATE DOCTOR
    def post(self, request):

        serializer = DoctorCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            doctor = create_new_doctor(
                serializer.validated_data
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor created successfully.",

                "doctor": {
                    "id":
                        str(doctor["_id"]),

                    "first_name":
                        doctor["first_name"],

                    "last_name":
                        doctor["last_name"],

                    "name":
                        f"{doctor['first_name']} "
                        f"{doctor['last_name']}",

                    "email":
                        doctor["email"],

                    "phone":
                        doctor["phone"],

                    "department":
                        doctor["department"],

                    "specialization":
                        doctor["specialization"],

                    "experience":
                        doctor["experience"],

                    "status":
                        doctor["status"],

                    "is_active":
                        doctor["is_active"],
                }
            },
            status=status.HTTP_201_CREATED
        )


class DoctorDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET SINGLE DOCTOR
    def get(self, request, doctor_id):

        doctor = get_doctor(
            doctor_id
        )

        if not doctor:

            return Response(
                {
                    "success": False,
                    "message":
                        "Doctor not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,

                "doctor": {
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

                    "department":
                        doctor.get(
                            "department",
                            ""
                        ),

                    "specialization":
                        doctor.get(
                            "specialization",
                            ""
                        ),

                    "experience":
                        doctor.get(
                            "experience",
                            0
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
            },
            status=status.HTTP_200_OK
        )

    # UPDATE DOCTOR
    def patch(self, request, doctor_id):

        serializer = DoctorUpdateSerializer(
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            updated_doctor = (
                update_existing_doctor(
                    doctor_id,
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not updated_doctor:

            return Response(
                {
                    "success": False,
                    "message":
                        "Doctor not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor updated successfully.",

                "doctor": {
                    "id":
                        str(updated_doctor["_id"]),

                    "first_name":
                        updated_doctor.get(
                            "first_name",
                            ""
                        ),

                    "last_name":
                        updated_doctor.get(
                            "last_name",
                            ""
                        ),

                    "name":
                        f"{updated_doctor.get('first_name', '')} "
                        f"{updated_doctor.get('last_name', '')}".strip(),

                    "email":
                        updated_doctor.get(
                            "email",
                            ""
                        ),

                    "phone":
                        updated_doctor.get(
                            "phone",
                            ""
                        ),

                    "department":
                        updated_doctor.get(
                            "department",
                            ""
                        ),

                    "specialization":
                        updated_doctor.get(
                            "specialization",
                            ""
                        ),

                    "experience":
                        updated_doctor.get(
                            "experience",
                            0
                        ),

                    "status":
                        updated_doctor.get(
                            "status",
                            "active"
                        ),

                    "is_active":
                        updated_doctor.get(
                            "is_active",
                            True
                        ),
                }
            },
            status=status.HTTP_200_OK
        )

    # DELETE DOCTOR
    def delete(self, request, doctor_id):

        doctor = get_doctor(
            doctor_id
        )

        if not doctor:

            return Response(
                {
                    "success": False,
                    "message":
                        "Doctor not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deleted = remove_doctor(
            doctor_id
        )

        if not deleted:

            return Response(
                {
                    "success": False,
                    "message":
                        "Unable to delete doctor."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Doctor deleted successfully."
            },
            status=status.HTTP_200_OK
        )





class PatientListView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        patients = get_patients()

        patient_list = []

        for patient in patients:

            patient_list.append({

                "id":
                    str(patient["_id"]),

                "first_name":
                    patient.get(
                        "first_name",
                        ""
                    ),

                "last_name":
                    patient.get(
                        "last_name",
                        ""
                    ),

                "name":
                    f"{patient.get('first_name', '')} "
                    f"{patient.get('last_name', '')}".strip(),

                "email":
                    patient.get(
                        "email",
                        ""
                    ),

                "phone":
                    patient.get(
                        "phone",
                        ""
                    ),

                "gender":
                    patient.get(
                        "gender",
                        ""
                    ),

                "date_of_birth":
                    patient.get(
                        "date_of_birth",
                        ""
                    ),

                "status":
                    patient.get(
                        "status",
                        "active"
                    ),

                "is_active":
                    patient.get(
                        "is_active",
                        True
                    ),

                "is_verified":
                    patient.get(
                        "is_verified",
                        False
                    ),

                "created_at":
                    patient.get(
                        "created_at"
                    ),
            })

        return Response(
            {
                "success": True,
                "count": len(patient_list),
                "patients": patient_list,
            },
            status=status.HTTP_200_OK
        )



    

class PatientDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET SINGLE PATIENT
    def get(
        self,
        request,
        patient_id
    ):

        patient = get_patient(
            patient_id
        )

        if not patient:

            return Response(
                {
                    "success": False,
                    "message":
                        "Patient not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,

                "patient": {
                    "id":
                        str(patient["_id"]),

                    "first_name":
                        patient.get(
                            "first_name",
                            ""
                        ),

                    "last_name":
                        patient.get(
                            "last_name",
                            ""
                        ),

                    "name":
                        f"{patient.get('first_name', '')} "
                        f"{patient.get('last_name', '')}".strip(),

                    "email":
                        patient.get(
                            "email",
                            ""
                        ),

                    "phone":
                        patient.get(
                            "phone",
                            ""
                        ),

                    "gender":
                        patient.get(
                            "gender",
                            ""
                        ),

                    "date_of_birth":
                        patient.get(
                            "date_of_birth",
                            ""
                        ),

                    "role":
                        patient.get(
                            "role",
                            "patient"
                        ),

                    "status":
                        patient.get(
                            "status",
                            "active"
                        ),

                    "is_active":
                        patient.get(
                            "is_active",
                            True
                        ),

                    "is_verified":
                        patient.get(
                            "is_verified",
                            False
                        ),

                    "created_at":
                        patient.get(
                            "created_at"
                        ),

                    "updated_at":
                        patient.get(
                            "updated_at"
                        ),
                }
            },
            status=status.HTTP_200_OK
        )

    # PUT
    def put(
        self,
        request,
        patient_id
    ):

        serializer = PatientUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            updated_patient = (
                update_existing_patient(
                    patient_id,
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not updated_patient:

            return Response(
                {
                    "success": False,
                    "message":
                        "Patient not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return self._patient_response(
            updated_patient,
            "Patient updated successfully."
        )

    # PATCH
    def patch(
        self,
        request,
        patient_id
    ):

        serializer = PatientUpdateSerializer(
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            updated_patient = (
                update_existing_patient(
                    patient_id,
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not updated_patient:

            return Response(
                {
                    "success": False,
                    "message":
                        "Patient not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return self._patient_response(
            updated_patient,
            "Patient updated successfully."
        )

    # DELETE
    def delete(
        self,
        request,
        patient_id
    ):

        patient = get_patient(
            patient_id
        )

        if not patient:

            return Response(
                {
                    "success": False,
                    "message":
                        "Patient not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deleted = remove_patient(
            patient_id
        )

        if not deleted:

            return Response(
                {
                    "success": False,
                    "message":
                        "Unable to delete patient."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Patient deleted successfully."
            },
            status=status.HTTP_200_OK
        )

    # COMMON RESPONSE
    def _patient_response(
        self,
        patient,
        message
    ):

        return Response(
            {
                "success": True,
                "message": message,

                "patient": {
                    "id":
                        str(patient["_id"]),

                    "first_name":
                        patient.get(
                            "first_name",
                            ""
                        ),

                    "last_name":
                        patient.get(
                            "last_name",
                            ""
                        ),

                    "name":
                        f"{patient.get('first_name', '')} "
                        f"{patient.get('last_name', '')}".strip(),

                    "email":
                        patient.get(
                            "email",
                            ""
                        ),

                    "phone":
                        patient.get(
                            "phone",
                            ""
                        ),

                    "gender":
                        patient.get(
                            "gender",
                            ""
                        ),

                    "date_of_birth":
                        patient.get(
                            "date_of_birth",
                            ""
                        ),

                    "status":
                        patient.get(
                            "status",
                            "active"
                        ),

                    "is_active":
                        patient.get(
                            "is_active",
                            True
                        ),
                }
            },
            status=status.HTTP_200_OK
        )





class AppointmentListCreateView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET ALL APPOINTMENTS
    def get(self, request):

        appointments = get_appointments()

        appointment_list = []

        for appointment in appointments:

            appointment_list.append({

                "id":
                    str(appointment["_id"]),

                "patient_id":
                    appointment.get(
                        "patient_id",
                        ""
                    ),

                "patient_name":
                    appointment.get(
                        "patient_name",
                        ""
                    ),

                "patient_email":
                    appointment.get(
                        "patient_email",
                        ""
                    ),

                "doctor_id":
                    appointment.get(
                        "doctor_id",
                        ""
                    ),

                "doctor_name":
                    appointment.get(
                        "doctor_name",
                        ""
                    ),

                "doctor_email":
                    appointment.get(
                        "doctor_email",
                        ""
                    ),

                "department":
                    appointment.get(
                        "department",
                        ""
                    ),

                "specialization":
                    appointment.get(
                        "specialization",
                        ""
                    ),

                "appointment_date":
                    appointment.get(
                        "appointment_date"
                    ),

                "appointment_time":
                    appointment.get(
                        "appointment_time"
                    ),

                "reason":
                    appointment.get(
                        "reason",
                        ""
                    ),

                "notes":
                    appointment.get(
                        "notes",
                        ""
                    ),

                "status":
                    appointment.get(
                        "status",
                        "pending"
                    ),

                "created_at":
                    appointment.get(
                        "created_at"
                    ),

                "updated_at":
                    appointment.get(
                        "updated_at"
                    ),
            })

        return Response(
            {
                "success": True,
                "count": len(appointment_list),
                "appointments": appointment_list,
            },
            status=status.HTTP_200_OK
        )

    # CREATE APPOINTMENT
    def post(self, request):

        serializer = AppointmentCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            appointment = (
                create_new_appointment(
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,

                "message":
                    "Appointment created successfully.",

                "appointment": self.serialize_appointment(
                    appointment
                )
            },
            status=status.HTTP_201_CREATED
        )

    # SERIALIZER
    def serialize_appointment(
        self,
        appointment
    ):

        return {

            "id":
                str(appointment["_id"]),

            "patient_id":
                appointment.get(
                    "patient_id",
                    ""
                ),

            "patient_name":
                appointment.get(
                    "patient_name",
                    ""
                ),

            "patient_email":
                appointment.get(
                    "patient_email",
                    ""
                ),

            "doctor_id":
                appointment.get(
                    "doctor_id",
                    ""
                ),

            "doctor_name":
                appointment.get(
                    "doctor_name",
                    ""
                ),

            "doctor_email":
                appointment.get(
                    "doctor_email",
                    ""
                ),

            "department":
                appointment.get(
                    "department",
                    ""
                ),

            "specialization":
                appointment.get(
                    "specialization",
                    ""
                ),

            "appointment_date":
                appointment.get(
                    "appointment_date"
                ),

            "appointment_time":
                appointment.get(
                    "appointment_time"
                ),

            "reason":
                appointment.get(
                    "reason",
                    ""
                ),

            "notes":
                appointment.get(
                    "notes",
                    ""
                ),

            "status":
                appointment.get(
                    "status",
                    "pending"
                ),

            "created_at":
                appointment.get(
                    "created_at"
                ),

            "updated_at":
                appointment.get(
                    "updated_at"
                ),
        }




class AppointmentDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET SINGLE APPOINTMENT
    def get(
        self,
        request,
        appointment_id
    ):

        appointment = get_appointment(
            appointment_id
        )

        if not appointment:

            return Response(
                {
                    "success": False,
                    "message":
                        "Appointment not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "appointment":
                    self.serialize_appointment(
                        appointment
                    )
            },
            status=status.HTTP_200_OK
        )

    # PUT
    def put(
        self,
        request,
        appointment_id
    ):

        serializer = AppointmentUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_appointment = (
            update_existing_appointment(
                appointment_id,
                serializer.validated_data
            )
        )

        if not updated_appointment:

            return Response(
                {
                    "success": False,
                    "message":
                        "Appointment not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "Appointment updated successfully.",
                "appointment":
                    self.serialize_appointment(
                        updated_appointment
                    )
            },
            status=status.HTTP_200_OK
        )

    # PATCH
    def patch(
        self,
        request,
        appointment_id
    ):

        serializer = AppointmentUpdateSerializer(
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_appointment = (
            update_existing_appointment(
                appointment_id,
                serializer.validated_data
            )
        )

        if not updated_appointment:

            return Response(
                {
                    "success": False,
                    "message":
                        "Appointment not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "Appointment updated successfully.",
                "appointment":
                    self.serialize_appointment(
                        updated_appointment
                    )
            },
            status=status.HTTP_200_OK
        )

    # DELETE
    def delete(
        self,
        request,
        appointment_id
    ):

        appointment = get_appointment(
            appointment_id
        )

        if not appointment:

            return Response(
                {
                    "success": False,
                    "message":
                        "Appointment not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deleted = remove_appointment(
            appointment_id
        )

        if not deleted:

            return Response(
                {
                    "success": False,
                    "message":
                        "Unable to delete appointment."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Appointment deleted successfully."
            },
            status=status.HTTP_200_OK
        )

    # SERIALIZER
    def serialize_appointment(
        self,
        appointment
    ):

        return {

            "id":
                str(appointment["_id"]),

            "patient_id":
                appointment.get(
                    "patient_id",
                    ""
                ),

            "patient_name":
                appointment.get(
                    "patient_name",
                    ""
                ),

            "patient_email":
                appointment.get(
                    "patient_email",
                    ""
                ),

            "doctor_id":
                appointment.get(
                    "doctor_id",
                    ""
                ),

            "doctor_name":
                appointment.get(
                    "doctor_name",
                    ""
                ),

            "doctor_email":
                appointment.get(
                    "doctor_email",
                    ""
                ),

            "department":
                appointment.get(
                    "department",
                    ""
                ),

            "specialization":
                appointment.get(
                    "specialization",
                    ""
                ),

            "appointment_date":
                appointment.get(
                    "appointment_date"
                ),

            "appointment_time":
                appointment.get(
                    "appointment_time"
                ),

            "reason":
                appointment.get(
                    "reason",
                    ""
                ),

            "notes":
                appointment.get(
                    "notes",
                    ""
                ),

            "status":
                appointment.get(
                    "status",
                    "pending"
                ),

            "created_at":
                appointment.get(
                    "created_at"
                ),

            "updated_at":
                appointment.get(
                    "updated_at"
                ),
        }




# DEPARTMENT LIST + CREATE
class DepartmentListCreateView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]


    # GET ALL DEPARTMENTS

    def get(self, request):

        departments = get_departments()

        department_list = []

        for department in departments:

            department_list.append(
                self.serialize_department(
                    department
                )
            )

        return Response(
            {
                "success": True,
                "count": len(department_list),
                "departments": department_list,
            },
            status=status.HTTP_200_OK
        )

    # CREATE DEPARTMENT
    def post(self, request):

        serializer = DepartmentCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            department = (
                create_new_department(
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Department created successfully.",
                "department":
                    self.serialize_department(
                        department
                    )
            },
            status=status.HTTP_201_CREATED
        )

    # SERIALIZER
    def serialize_department(
        self,
        department
    ):

        return {

            "id":
                str(department["_id"]),

            "name":
                department.get(
                    "name",
                    ""
                ),

            "description":
                department.get(
                    "description",
                    ""
                ),

            "status":
                department.get(
                    "status",
                    "active"
                ),

            "created_at":
                department.get(
                    "created_at"
                ),

            "updated_at":
                department.get(
                    "updated_at"
                ),
        }






# DEPARTMENT DETAIL
class DepartmentDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET
    def get(
        self,
        request,
        department_id
    ):

        department = get_department(
            department_id
        )

        if not department:

            return Response(
                {
                    "success": False,
                    "message":
                        "Department not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "department":
                    self.serialize_department(
                        department
                    )
            },
            status=status.HTTP_200_OK
        )

    # PUT
    def put(
        self,
        request,
        department_id
    ):

        serializer = DepartmentUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            department = (
                update_existing_department(
                    department_id,
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not department:

            return Response(
                {
                    "success": False,
                    "message":
                        "Department not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "Department updated successfully.",
                "department":
                    self.serialize_department(
                        department
                    )
            },
            status=status.HTTP_200_OK
        )

    # PATCH
    def patch(
        self,
        request,
        department_id
    ):

        serializer = DepartmentUpdateSerializer(
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            department = (
                update_existing_department(
                    department_id,
                    serializer.validated_data
                )
            )

        except ValueError as error:

            return Response(
                {
                    "success": False,
                    "message": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not department:

            return Response(
                {
                    "success": False,
                    "message":
                        "Department not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "Department updated successfully.",
                "department":
                    self.serialize_department(
                        department
                    )
            },
            status=status.HTTP_200_OK
        )

    # DELETE
    def delete(
        self,
        request,
        department_id
    ):

        department = get_department(
            department_id
        )

        if not department:

            return Response(
                {
                    "success": False,
                    "message":
                        "Department not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        deleted = remove_department(
            department_id
        )

        if not deleted:

            return Response(
                {
                    "success": False,
                    "message":
                        "Unable to delete department."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "Department deleted successfully."
            },
            status=status.HTTP_200_OK
        )

    # SERIALIZER
    def serialize_department(
        self,
        department
    ):

        return {

            "id":
                str(department["_id"]),

            "name":
                department.get(
                    "name",
                    ""
                ),

            "description":
                department.get(
                    "description",
                    ""
                ),

            "status":
                department.get(
                    "status",
                    "active"
                ),

            "created_at":
                department.get(
                    "created_at"
                ),

            "updated_at":
                department.get(
                    "updated_at"
                ),
        }





# ADMIN USERS
class AdminUserListView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        users = get_users()

        user_list = []

        for user in users:

            user_list.append(
                self.serialize_user(user)
            )

        return Response(
            {
                "success": True,
                "count": len(user_list),
                "users": user_list,
            },
            status=status.HTTP_200_OK
        )

    def serialize_user(
        self,
        user
    ):

        return {

            "id":
                str(user["_id"]),

            "first_name":
                user.get(
                    "first_name",
                    ""
                ),

            "last_name":
                user.get(
                    "last_name",
                    ""
                ),

            "email":
                user.get(
                    "email",
                    ""
                ),

            "phone":
                user.get(
                    "phone",
                    ""
                ),

            "role":
                user.get(
                    "role",
                    ""
                ),

            "is_active":
                user.get(
                    "is_active",
                    True
                ),

            "is_verified":
                user.get(
                    "is_verified",
                    False
                ),

            "created_at":
                user.get(
                    "created_at"
                ),
        }



class AdminUserDetailView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    # GET SINGLE USER
    def get(
        self,
        request,
        user_id
    ):

        user = get_user(
            user_id
        )

        if not user:

            return Response(
                {
                    "success": False,
                    "message":
                        "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "user":
                    self.serialize_user(user)
            },
            status=status.HTTP_200_OK
        )

    # PATCH USER
    def patch(
        self,
        request,
        user_id
    ):

        serializer = AdminUserUpdateSerializer(
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        updated_user = (
            update_existing_user(
                user_id,
                serializer.validated_data
            )
        )

        if not updated_user:

            return Response(
                {
                    "success": False,
                    "message":
                        "User not found or nothing to update."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message":
                    "User updated successfully.",
                "user":
                    self.serialize_user(
                        updated_user
                    )
            },
            status=status.HTTP_200_OK
        )

    # DELETE USER
    def delete(
        self,
        request,
        user_id
    ):

        user = get_user(
            user_id
        )

        if not user:

            return Response(
                {
                    "success": False,
                    "message":
                        "User not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Prevent admin from deleting themselves

        if str(user["_id"]) == str(
            request.user["_id"]
        ):

            return Response(
                {
                    "success": False,
                    "message":
                        "You cannot delete your own account."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted = remove_user(
            user_id
        )

        if not deleted:

            return Response(
                {
                    "success": False,
                    "message":
                        "Unable to delete user."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "success": True,
                "message":
                    "User deleted successfully."
            },
            status=status.HTTP_200_OK
        )

    # SERIALIZER
    def serialize_user(
        self,
        user
    ):

        return {

            "id":
                str(user["_id"]),

            "first_name":
                user.get(
                    "first_name",
                    ""
                ),

            "last_name":
                user.get(
                    "last_name",
                    ""
                ),

            "email":
                user.get(
                    "email",
                    ""
                ),

            "phone":
                user.get(
                    "phone",
                    ""
                ),

            "role":
                user.get(
                    "role",
                    ""
                ),

            "is_active":
                user.get(
                    "is_active",
                    True
                ),

            "is_verified":
                user.get(
                    "is_verified",
                    False
                ),

            "created_at":
                user.get(
                    "created_at"
                ),
        }





# ADMIN DASHBOARD STATISTICS
class AdminDashboardStatsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        statistics = (
            get_admin_dashboard_statistics()
        )

        serializer = DashboardStatsSerializer(
            data=statistics
        )

        serializer.is_valid(
            raise_exception=True
        )

        return Response(
            {
                "success": True,
                "message":
                    "Dashboard statistics retrieved successfully.",
                "statistics":
                    serializer.validated_data
            },
            status=status.HTTP_200_OK
        )




# RECENT APPOINTMENTS
class AdminRecentAppointmentsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAdminUser
    ]

    def get(self, request):

        appointments = (
            get_admin_recent_appointments(
                limit=5
            )
        )

        appointment_list = []

        for appointment in appointments:

            appointment_data = {

                "id":
                    str(
                        appointment["_id"]
                    ),

                "patient_id":
                    str(
                        appointment.get(
                            "patient_id",
                            ""
                        )
                    ),

                "patient_name":
                    appointment.get(
                        "patient_name",
                        ""
                    ),

                "patient_email":
                    appointment.get(
                        "patient_email",
                        ""
                    ),

                "doctor_id":
                    str(
                        appointment.get(
                            "doctor_id",
                            ""
                        )
                    ),

                "doctor_name":
                    appointment.get(
                        "doctor_name",
                        ""
                    ),

                "doctor_email":
                    appointment.get(
                        "doctor_email",
                        ""
                    ),

                "department":
                    appointment.get(
                        "department",
                        ""
                    ),

                "specialization":
                    appointment.get(
                        "specialization",
                        ""
                    ),

                "appointment_date":
                    appointment.get(
                        "appointment_date",
                        ""
                    ),

                "appointment_time":
                    appointment.get(
                        "appointment_time",
                        ""
                    ),

                "reason":
                    appointment.get(
                        "reason",
                        ""
                    ),

                "notes":
                    appointment.get(
                        "notes",
                        ""
                    ),

                "status":
                    appointment.get(
                        "status",
                        "pending"
                    ),

                "created_at":
                    (
                        appointment.get(
                            "created_at"
                        ).isoformat()
                        if appointment.get(
                            "created_at"
                        )
                        else ""
                    ),
            }

            serializer = RecentAppointmentSerializer(
                data=appointment_data
            )

            serializer.is_valid(
                raise_exception=True
            )

            appointment_list.append(
                serializer.validated_data
            )

        return Response(
            {
                "success": True,

                "count":
                    len(appointment_list),

                "appointments":
                    appointment_list,
            },

            status=status.HTTP_200_OK
        )






class AdminReportsView(APIView):

    authentication_classes = [
        MongoJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        print("================================")
        print("REPORT API STARTED")
        print("================================")

        period = request.query_params.get(
            "period",
            "This Month"
        )

        print("Requested period:", period)

        serializer = ReportSerializer(
            data={
                "period": period
            }
        )

        serializer.is_valid(
            raise_exception=True
        )

        period = serializer.validated_data[
            "period"
        ]

        print("Validated period:", period)

        report = generate_report(
            period
        )

        print("Report generated successfully")

        return Response(
            {
                "success": True,
                "message":
                    "Report generated successfully.",
                "report": report
            },
            status=status.HTTP_200_OK
        )