from django.urls import path

from .views import (
    DoctorListCreateView,
    DoctorDetailView,
    PatientListView,
    PatientDetailView,
    AppointmentListCreateView,
    AppointmentDetailView,
    DepartmentListCreateView,
    DepartmentDetailView,
    AdminUserListView,
    AdminUserDetailView,
    AdminDashboardStatsView,
    AdminRecentAppointmentsView,
    AdminReportsView,
)


urlpatterns = [

    # Doctors
    path(
        "doctors/",
        DoctorListCreateView.as_view(),
        name="admin-doctors"
    ),

    path(
        "doctors/<str:doctor_id>/",
        DoctorDetailView.as_view(),
        name="admin-doctor-detail"
    ),


    # Patinets 
     path(
        "patients/",
        PatientListView.as_view(),
        name="admin-patients"
    ),

    path(
        "patients/<str:patient_id>/",
        PatientDetailView.as_view(),
        name="admin-patient-detail"
    ),


    # APPOINTMENTS
    path(
        "appointments/",
         AppointmentListCreateView.as_view(),
         name="admin-appointments"
    ),

    path(
        "appointments/<str:appointment_id>/",
         AppointmentDetailView.as_view(),
         name="admin-appointment-detail"
    ),



    # DEPARTMENTS
    path(
       "departments/",
       DepartmentListCreateView.as_view(),
       name="admin-departments"
    ),

    path(
       "departments/<str:department_id>/",
        DepartmentDetailView.as_view(),
       name="admin-department-detail"
    ),

    
    # Users 
    path(
        "users/",
        AdminUserListView.as_view(),
        name="admin-users"
    ),

    path(
       "users/<str:user_id>/",
        AdminUserDetailView.as_view(),
        name="admin-user-detail"
    ),


    # dashboard stats 
    path(
       "dashboard/stats/",
       AdminDashboardStatsView.as_view(),
       name="admin-dashboard-stats"
    ),


    path(
       "dashboard/recent-appointments/",
       AdminRecentAppointmentsView.as_view(),
       name="admin-recent-appointments"
    ),


    # reports 
     path(
        "reports/",
        AdminReportsView.as_view(),
        name="admin-reports"
    ),
    

]