from django.urls import path

from .views import (
  DoctorDashboardView,
  DoctorAppointmentsView,
  DoctorScheduleView,
  DoctorProfileView,

  DoctorPatientsView,
    DoctorPatientDetailView,
    DoctorPatientAppointmentsView,

    DoctorMedicalRecordsView,
    DoctorMedicalRecordDetailView,
)



urlpatterns = [
    path(
        "dashboard/",
        DoctorDashboardView.as_view(),
        name="doctor-dashboard"
    ),

    path(
        "appointments/",
        DoctorAppointmentsView.as_view(),
        name="doctor-appointments"
    ),

    path(
        "schedule/",
        DoctorScheduleView.as_view(),
        name="doctor-schedule"
    ),

    path(
        "profile/",
        DoctorProfileView.as_view(),
        name="doctor-profile"
    ),


    # Patients 
     path(
        "patients/",
        DoctorPatientsView.as_view(),
        name="doctor-patients"
    ),


    #  Patient Details 
     path(
        "patients/<str:patient_id>/",
        DoctorPatientDetailView.as_view(),
        name="doctor-patient-detail"
    ),

    # PATIENT APPOINTMENTS
    path(
        "patients/<str:patient_id>/appointments/",
        DoctorPatientAppointmentsView.as_view(),
        name="doctor-patient-appointments"
    ),


     # MEDICAL RECORDS
    path(
        "medical-records/",
        DoctorMedicalRecordsView.as_view(),
        name="doctor-medical-records"
    ),

    # MEDICAL RECORD DETAIL
    path(
        "medical-records/<str:record_id>/",
        DoctorMedicalRecordDetailView.as_view(),
        name="doctor-medical-record-detail"
    ),
]