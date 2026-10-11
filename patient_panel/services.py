from .repositories import (
    get_patient_by_id,
    get_patient_appointments,
    get_patient_appointment_count,
    get_patient_upcoming_count,
    get_patient_completed_count,
    get_patient_cancelled_count,
    get_doctor_count,
    get_active_department_count,

    get_upcoming_appointment,
    get_patient_appointments,
    get_patient_appointment_by_id,
    get_patient_appointment_counts,
    cancel_patient_appointment,

    get_patient_medical_records,
    get_patient_medical_record_by_id,
    get_patient_medical_record_counts,
)

from .serializers import MedicalRecordSerializer


ALLOWED_STATUS_FILTERS = [
    "upcoming",
    "pending",
    "confirmed",
    "completed",
    "cancelled",
]


def get_full_name(first_name, last_name):
    """
    Create patient's full name.
    """

    return (
        f"{first_name or ''} {last_name or ''}"
    ).strip()


def serialize_appointment(appointment):
    """
    Convert MongoDB appointment document
    into API response format.
    """

    return {
        "id": str(appointment.get("_id")),

        "patient_id": appointment.get(
            "patient_id",
            ""
        ),

        "patient_name": appointment.get(
            "patient_name",
            ""
        ),

        "patient_email": appointment.get(
            "patient_email",
            ""
        ),

        "doctor_id": appointment.get(
            "doctor_id",
            ""
        ),

        "doctor_name": appointment.get(
            "doctor_name",
            ""
        ),

        "doctor_email": appointment.get(
            "doctor_email",
            ""
        ),

        "department": appointment.get(
            "department",
            ""
        ),

        "specialization": appointment.get(
            "specialization",
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

        "notes": appointment.get(
            "notes",
            ""
        ),

        "status": appointment.get(
            "status",
            ""
        ),

        "created_at": appointment.get(
            "created_at"
        ),

        "updated_at": appointment.get(
            "updated_at"
        ),
    }


def get_patient_dashboard(patient_id):
    """
    Get complete patient dashboard data.
    """

    # ---------------------------------
    # Patient
    # ---------------------------------

    patient = get_patient_by_id(patient_id)

    if not patient:
        return None

    full_name = get_full_name(
        patient.get("first_name"),
        patient.get("last_name")
    )

    # ---------------------------------
    # Recent appointments
    # ---------------------------------

    appointments = get_patient_appointments(
        patient_id,
        limit=5
    )

    recent_appointments = [
        serialize_appointment(appointment)
        for appointment in appointments
    ]

    # ---------------------------------
    # Upcoming appointment
    # ---------------------------------

    upcoming_appointment = get_upcoming_appointment(
        patient_id
    )

    # ---------------------------------
    # Dashboard data
    # ---------------------------------

    data = {
        "patient": {
            "id": str(patient.get("_id")),

            "first_name": patient.get(
                "first_name",
                ""
            ),

            "last_name": patient.get(
                "last_name",
                ""
            ),

            "full_name": full_name,

            "email": patient.get(
                "email",
                ""
            ),

            "phone": patient.get(
                "phone",
                ""
            ),

            "gender": patient.get(
                "gender",
                ""
            ),
        },

        "doctor": None,

        "quick_actions": {
            "appointments": get_patient_appointment_count(
                patient_id
            ),

            "doctors": get_doctor_count(),

            "departments": get_active_department_count(),
        },

        "recent_appointments": recent_appointments,

        "health_summary": {
            "gender": patient.get(
                "gender",
                ""
            )
        },

        "appointment_reminder": None,


        "appointment_summary": {
    "total": get_patient_appointment_count(
        patient_id
    ),

    "upcoming": get_patient_upcoming_count(
        patient_id
    ),

    "completed": get_patient_completed_count(
        patient_id
    ),

    "cancelled": get_patient_cancelled_count(
        patient_id
    ),
},
    }

    # ---------------------------------
    # Doctor / reminder
    # ---------------------------------

    if upcoming_appointment:

        data["doctor"] = {
            "id": upcoming_appointment.get(
                "doctor_id",
                ""
            ),

            "name": upcoming_appointment.get(
                "doctor_name",
                ""
            ),

            "email": upcoming_appointment.get(
                "doctor_email",
                ""
            ),

            "department": upcoming_appointment.get(
                "department",
                ""
            ),

            "specialization": upcoming_appointment.get(
                "specialization",
                ""
            ),

            "status": upcoming_appointment.get(
                "status",
                ""
            ),
        }

        data["appointment_reminder"] = {
            "has_reminder": True,

            "appointment_id": str(
                upcoming_appointment.get("_id")
            ),

            "doctor_name": upcoming_appointment.get(
                "doctor_name",
                ""
            ),

            "department": upcoming_appointment.get(
                "department",
                ""
            ),

            "specialization": upcoming_appointment.get(
                "specialization",
                ""
            ),

            "date": upcoming_appointment.get(
                "appointment_date",
                ""
            ),

            "time": upcoming_appointment.get(
                "appointment_time",
                ""
            ),

            "status": upcoming_appointment.get(
                "status",
                ""
            ),
        }

    else:

        data["appointment_reminder"] = {
            "has_reminder": False
        }

    return data






def serialize_appointment(appointment):
    """
    Convert MongoDB appointment document
    into API-friendly response.
    """

    return {
        "id": str(
            appointment.get("_id")
        ),

        "patient_id": appointment.get(
            "patient_id",
            ""
        ),

        "patient_name": appointment.get(
            "patient_name",
            ""
        ),

        "patient_email": appointment.get(
            "patient_email",
            ""
        ),

        "doctor_id": appointment.get(
            "doctor_id",
            ""
        ),

        "doctor_name": appointment.get(
            "doctor_name",
            ""
        ),

        "doctor_email": appointment.get(
            "doctor_email",
            ""
        ),

        "department": appointment.get(
            "department",
            ""
        ),

        "specialization": appointment.get(
            "specialization",
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

        "notes": appointment.get(
            "notes",
            ""
        ),

        "status": appointment.get(
            "status",
            ""
        ),

        "created_at": appointment.get(
            "created_at"
        ),

        "updated_at": appointment.get(
            "updated_at"
        ),
    }


def get_patient_appointments_data(
    patient_id,
    status_filter=None
):
    """
    Get appointment history and summary.
    """

    appointments = get_patient_appointments(
        patient_id,
        status_filter=status_filter
    )

    summary = get_patient_appointment_counts(
        patient_id
    )

    return {
        "summary": summary,

        "appointments": [
            serialize_appointment(appointment)
            for appointment in appointments
        ]
    }


def get_patient_appointment_details(
    patient_id,
    appointment_id
):
    """
    Get details of one patient's appointment.
    """

    appointment = get_patient_appointment_by_id(
        patient_id,
        appointment_id
    )

    if not appointment:
        return None

    return serialize_appointment(
        appointment
    )


def cancel_appointment(
    patient_id,
    appointment_id
):
    """
    Cancel patient's appointment.
    """

    appointment = get_patient_appointment_by_id(
        patient_id,
        appointment_id
    )

    if not appointment:
        return {
            "success": False,
            "message": "Appointment not found."
        }

    current_status = str(
        appointment.get("status", "")
    ).lower()

    # Already cancelled
    if current_status == "cancelled":

        return {
            "success": False,
            "message": "Appointment is already cancelled."
        }

    # Completed cannot be cancelled
    if current_status == "completed":

        return {
            "success": False,
            "message": "Completed appointment cannot be cancelled."
        }

    updated = cancel_patient_appointment(
        patient_id,
        appointment_id
    )

    if not updated:

        return {
            "success": False,
            "message": "Unable to cancel appointment."
        }

    return {
        "success": True,
        "message": "Appointment cancelled successfully."
    }




    # MEDICAL RECORD SERIALIZER HELPER
# =========================================================

def serialize_medical_record(record):
    """
    Convert MongoDB medical record into API-friendly data.
    """

    return {
        "id": str(record.get("_id")),

        "patient_id": str(
            record.get("patient_id", "")
        ),

        "title": record.get("title", ""),

        "type": record.get("type", ""),

        "description": record.get(
            "description",
            ""
        ),

        "doctor_id": str(
            record.get("doctor_id", "")
        ),

        "doctor_name": record.get(
            "doctor_name",
            ""
        ),

        "doctor_email": record.get(
            "doctor_email",
            ""
        ),

        "specialization": record.get(
            "specialization",
            ""
        ),

        "department": record.get(
            "department",
            ""
        ),

        "date": record.get(
            "date",
            ""
        ),

        "status": record.get(
            "status",
            ""
        ),

        "notes": record.get(
            "notes",
            ""
        ),

        "file_name": record.get(
            "file_name"
        ),

        "file_url": record.get(
            "file_url"
        ),

        "created_at": (
            record.get("created_at").isoformat()
            if record.get("created_at")
            else None
        ),

        "updated_at": (
            record.get("updated_at").isoformat()
            if record.get("updated_at")
            else None
        )
    }


# =========================================================
# GET MEDICAL RECORDS
# =========================================================

def get_patient_medical_records_data(
    patient_id,
    record_type=None
):
    """
    Get patient's medical records with summary.
    """

    records = get_patient_medical_records(
        patient_id,
        record_type=record_type
    )

    summary = get_patient_medical_record_counts(
        patient_id
    )

    serialized_records = [
        serialize_medical_record(record)
        for record in records
    ]

    return {
        "summary": summary,
        "records": serialized_records
    }


# =========================================================
# GET SINGLE MEDICAL RECORD
# =========================================================

def get_patient_medical_record_data(
    patient_id,
    record_id
):
    """
    Get a single medical record.
    """

    record = get_patient_medical_record_by_id(
        patient_id,
        record_id
    )

    if not record:
        return None

    return serialize_medical_record(record)


# =========================================================
# GET DOWNLOAD INFORMATION
# =========================================================

def get_medical_record_download_data(
    patient_id,
    record_id
):
    """
    Get download information for a medical record.
    """

    record = get_patient_medical_record_by_id(
        patient_id,
        record_id
    )

    if not record:
        return None

    return {
        "id": str(record.get("_id")),
        "file_name": record.get("file_name"),
        "file_url": record.get("file_url")
    }