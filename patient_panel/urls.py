from django.urls import path

from .views import (
    PatientDashboardView,
    PatientAppointmentsView,
    PatientAppointmentDetailView,
    CancelPatientAppointmentView,

    PatientMedicalRecordsView,
    PatientMedicalRecordDetailView,
    PatientMedicalRecordDownloadView,
)


urlpatterns = [
    path(
        "dashboard/",
        PatientDashboardView.as_view(),
        name="patient-dashboard"
    ),


     # My Appointments
    path(
        "appointments/",
        PatientAppointmentsView.as_view(),
        name="patient-appointments"
    ),

    # Appointment details
    path(
        "appointments/<str:appointment_id>/",
        PatientAppointmentDetailView.as_view(),
        name="patient-appointment-detail"
    ),

    # Cancel appointment
    path(
        "appointments/<str:appointment_id>/cancel/",
        CancelPatientAppointmentView.as_view(),
        name="patient-appointment-cancel"
    ),


    # Medical records 
     path(
        "medical-records/",
        PatientMedicalRecordsView.as_view(),
        name="patient-medical-records"
    ),

    path(
        "medical-records/<str:record_id>/",
        PatientMedicalRecordDetailView.as_view(),
        name="patient-medical-record-detail"
    ),


    path(
        "medical-records/<str:record_id>/download/",
        PatientMedicalRecordDownloadView.as_view(),
        name="patient-medical-record-download"
    ),
]