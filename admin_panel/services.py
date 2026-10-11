from datetime import datetime, timezone

from django.contrib.auth.hashers import make_password

from .repositories import (
    create_doctor,
    get_all_doctors,
    get_doctor_by_id,
    get_doctor_by_email,
    update_doctor,
    delete_doctor,

    get_all_patients,
    get_patient_by_id,
    get_patient_by_email,
    update_patient,
    delete_patient,

    create_appointment,
    get_all_appointments,
    get_appointment_by_id,
    update_appointment,
    delete_appointment,

    create_department,
    get_all_departments,
    get_department_by_id,
    get_department_by_name,
    update_department,
    delete_department,


    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,

    get_dashboard_statistics,
    get_recent_appointments,

    get_period_range,
    get_appointment_count,
    get_completed_appointment_count,
    get_total_patients,
    get_new_patients,
    get_total_doctors,
    get_active_doctors,
    get_doctor_performance,
    get_department_reports,
    get_appointment_trend,
)


def create_new_doctor(data):

    email = data["email"].lower().strip()

    existing_doctor = get_doctor_by_email(
        email
    )

    if existing_doctor:

        raise ValueError(
            "A doctor with this email already exists."
        )

    doctor = {

        "first_name":
            data["first_name"].strip(),

        "last_name":
            data["last_name"].strip(),

        "email":
            email,

        "phone":
            data["phone"].strip(),

        "password":
            make_password(
                data["password"]
            ),

        # Backend controlled
        "role": "doctor",

        "department":
            data["department"].strip(),

        "specialization":
            data["specialization"].strip(),

        "experience":
            data["experience"],

        "status": "active",

        "is_active": True,

        "is_verified": True,

        "created_at":
            datetime.now(timezone.utc),

        "updated_at":
            datetime.now(timezone.utc),
    }

    return create_doctor(
        doctor
    )


def get_doctors():

    return get_all_doctors()


def get_doctor(doctor_id):

    return get_doctor_by_id(
        doctor_id
    )


def update_existing_doctor(
    doctor_id,
    data
):

    doctor = get_doctor_by_id(
        doctor_id
    )

    if not doctor:

        return None

    update_data = {}

    allowed_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "department",
        "specialization",
        "experience",
        "status",
    ]

    for field in allowed_fields:

        if field in data:

            value = data[field]

            if isinstance(value, str):
                value = value.strip()

            update_data[field] = value

    if "email" in update_data:

        existing_doctor = get_doctor_by_email(
            update_data["email"]
        )

        if (
            existing_doctor
            and str(existing_doctor["_id"])
            != str(doctor["_id"])
        ):

            raise ValueError(
                "A doctor with this email already exists."
            )

    # Keep status and is_active synchronized
    if "status" in update_data:

        update_data["is_active"] = (
            update_data["status"] == "active"
        )

    update_data["updated_at"] = (
        datetime.now(timezone.utc)
    )

    if not update_data:

        return None

    return update_doctor(
        doctor_id,
        update_data
    )


def remove_doctor(doctor_id):

    return delete_doctor(
        doctor_id
    )





# PATIENT SERVICES
def get_patients():

    return get_all_patients()


def get_patient(patient_id):

    return get_patient_by_id(
        patient_id
    )


def update_existing_patient(
    patient_id,
    data
):

    patient = get_patient_by_id(
        patient_id
    )

    if not patient:

        return None

    update_data = {}

    allowed_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "gender",
        "date_of_birth",
        "status",
    ]

    for field in allowed_fields:

        if field in data:

            value = data[field]

            if isinstance(value, str):
                value = value.strip()

            update_data[field] = value

    # Check email uniqueness
    if "email" in update_data:

        existing_patient = get_patient_by_email(
            update_data["email"]
        )

        if (
            existing_patient
            and str(existing_patient["_id"])
            != str(patient["_id"])
        ):

            raise ValueError(
                "A patient with this email already exists."
            )

    # Keep status and is_active synchronized
    if "status" in update_data:

        update_data["is_active"] = (
            update_data["status"] == "active"
        )

    update_data["updated_at"] = (
        datetime.now(timezone.utc)
    )

    if not update_data:

        return None

    return update_patient(
        patient_id,
        update_data
    )


def remove_patient(patient_id):

    return delete_patient(
        patient_id
    )




# APPOINTMENT SERVICES
def create_new_appointment(data):

    patient = get_patient_by_id(
        data["patient_id"]
    )

    if not patient:

        raise ValueError(
            "Patient not found."
        )

    doctor = get_doctor_by_id(
        data["doctor_id"]
    )

    if not doctor:

        raise ValueError(
            "Doctor not found."
        )

    appointment_data = {

        "patient_id":
            str(patient["_id"]),

        "patient_name":
            f"{patient.get('first_name', '')} "
            f"{patient.get('last_name', '')}".strip(),

        "patient_email":
            patient.get(
                "email",
                ""
            ),

        "doctor_id":
            str(doctor["_id"]),

        "doctor_name":
            f"{doctor.get('first_name', '')} "
            f"{doctor.get('last_name', '')}".strip(),

        "doctor_email":
            doctor.get(
                "email",
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

       "appointment_date":
    data["appointment_date"].isoformat(),

"appointment_time":
    data["appointment_time"].isoformat(),

        "reason":
            data.get(
                "reason",
                ""
            ),

        "notes":
            data.get(
                "notes",
                ""
            ),

        "status":
            data.get(
                "status",
                "pending"
            ),

        "created_at":
            datetime.now(timezone.utc),

        "updated_at":
            datetime.now(timezone.utc),
    }

    return create_appointment(
        appointment_data
    )


def get_appointments():

    return get_all_appointments()


def get_appointment(
    appointment_id
):

    return get_appointment_by_id(
        appointment_id
    )


def update_existing_appointment(
    appointment_id,
    data
):

    appointment = get_appointment_by_id(
        appointment_id
    )

    if not appointment:

        return None

    update_data = {}

    allowed_fields = [
        "appointment_date",
        "appointment_time",
        "reason",
        "notes",
        "status",
    ]

    for field in allowed_fields:

        if field in data:

            update_data[field] = data[field]

    if not update_data:

        return None

    update_data["updated_at"] = (
        datetime.now(timezone.utc)
    )

    return update_appointment(
        appointment_id,
        update_data
    )


def remove_appointment(
    appointment_id
):

    return delete_appointment(
        appointment_id
    )



# DEPARTMENT SERVICES
def create_new_department(data):

    name = data["name"].strip()

    existing_department = get_department_by_name(
        name
    )

    if existing_department:

        raise ValueError(
            "A department with this name already exists."
        )

    department_data = {

        "name":
            name,

        "description":
            data.get(
                "description",
                ""
            ).strip(),

        "status":
            data.get(
                "status",
                "active"
            ),

        "created_at":
            datetime.now(timezone.utc),

        "updated_at":
            datetime.now(timezone.utc),
    }

    return create_department(
        department_data
    )


def get_departments():

    return get_all_departments()


def get_department(
    department_id
):

    return get_department_by_id(
        department_id
    )


def update_existing_department(
    department_id,
    data
):

    department = get_department_by_id(
        department_id
    )

    if not department:

        return None

    update_data = {}

    if "name" in data:

        name = data["name"].strip()

        existing_department = (
            get_department_by_name(name)
        )

        if (
            existing_department
            and str(existing_department["_id"])
            != str(department["_id"])
        ):

            raise ValueError(
                "A department with this name already exists."
            )

        update_data["name"] = name

    if "description" in data:

        update_data["description"] = (
            data["description"].strip()
        )

    if "status" in data:

        update_data["status"] = data["status"]

    if not update_data:

        return None

    update_data["updated_at"] = (
        datetime.now(timezone.utc)
    )

    return update_department(
        department_id,
        update_data
    )


def remove_department(
    department_id
):

    return delete_department(
        department_id
    )




# ADMIN USER SERVICES
def get_users():

    return get_all_users()


def get_user(
    user_id
):

    return get_user_by_id(
        user_id
    )


def update_existing_user(
    user_id,
    data
):

    user = get_user_by_id(
        user_id
    )

    if not user:

        return None

    update_data = {}

    if "first_name" in data:

        update_data["first_name"] = (
            data["first_name"].strip()
        )

    if "last_name" in data:

        update_data["last_name"] = (
            data["last_name"].strip()
        )

    if "email" in data:

        update_data["email"] = (
            data["email"].lower().strip()
        )

    if "phone" in data:

        update_data["phone"] = (
            data["phone"].strip()
        )

    if "role" in data:

        update_data["role"] = data["role"]

    if "is_active" in data:

        update_data["is_active"] = (
            data["is_active"]
        )

    if not update_data:

        return None

    update_data["updated_at"] = (
        datetime.now(timezone.utc)
    )

    return update_user(
        user_id,
        update_data
    )


def remove_user(
    user_id
):

    return delete_user(
        user_id
    )




# DASHBOARD STATISTICS SERVICE
def get_admin_dashboard_statistics():

    return get_dashboard_statistics()



# RECENT APPOINTMENTS SERVICE
def get_admin_recent_appointments(
    limit=5
):

    return get_recent_appointments(
        limit
    )




# REPORT SERVICE
def generate_report(period="This Month"):

    (
        start_date,
        end_date,
        previous_start,
        previous_end
    ) = get_period_range(period)

    # --------------------------------------------------------
    # APPOINTMENTS
    # --------------------------------------------------------

    total_appointments = get_appointment_count(
        start_date,
        end_date
    )

    completed_appointments = (
        get_completed_appointment_count(
            start_date,
            end_date
        )
    )

    previous_appointments = get_appointment_count(
        previous_start,
        previous_end
    )

    completion_rate = 0

    if total_appointments > 0:

        completion_rate = round(
            (
                completed_appointments
                / total_appointments
            ) * 100,
            2
        )

    appointment_change = 0

    if previous_appointments > 0:

        appointment_change = round(
            (
                (
                    total_appointments
                    - previous_appointments
                )
                / previous_appointments
            ) * 100,
            2
        )

    # --------------------------------------------------------
    # PATIENTS
    # --------------------------------------------------------

    total_patients = get_total_patients()

    new_patients = get_new_patients(
        start_date,
        end_date
    )

    # --------------------------------------------------------
    # DOCTORS
    # --------------------------------------------------------

    total_doctors = get_total_doctors()

    active_doctors = get_active_doctors()

    # --------------------------------------------------------
    # TRENDS
    # --------------------------------------------------------

    appointment_trend = get_appointment_trend(
        start_date,
        end_date
    )

    # --------------------------------------------------------
    # DEPARTMENTS
    # --------------------------------------------------------

    department_reports = get_department_reports(
        start_date,
        end_date
    )

    # --------------------------------------------------------
    # DOCTOR PERFORMANCE
    # --------------------------------------------------------

    doctor_reports = get_doctor_performance(
        start_date,
        end_date
    )

    return {

        "period": period,

        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },

        "metrics": {

            "totalAppointments":
                total_appointments,

            "completedAppointments":
                completed_appointments,

            "completionRate":
                completion_rate,

            "appointmentChange":
                appointment_change,

            "totalPatients":
                total_patients,

            "newPatients":
                new_patients,

            "activeDoctors":
                active_doctors,

            "totalDoctors":
                total_doctors
        },

        "appointmentTrend":
            appointment_trend,

        "departmentReports":
            department_reports,

        "doctorReports":
            doctor_reports
    }