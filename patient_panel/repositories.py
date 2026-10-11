from bson import ObjectId
from bson.errors import InvalidId

from config.database import db


# Collections
users_collection = db["users"]
departments_collection = db["departments"]
appointments_collection = db["appointments"]
medical_records_collection = db["medical_records"]



# =========================================================
# PATIENT
# =========================================================

def get_patient_by_id(patient_id):
    """
    Get patient from users collection.
    """

    return users_collection.find_one({
        "_id": patient_id,
        "role": "patient"
    })


# =========================================================
# APPOINTMENTS
# =========================================================

def get_patient_appointments(
    patient_id,
    limit=None,
    status_filter=None
):
    """
    Get appointments belonging to the logged-in patient.

    Used by:
    - Patient Dashboard
    - Patient Appointments page
    - Appointment status filters

    patient_id is stored as a string inside appointments.
    """

    query = {
        "patient_id": str(patient_id)
    }

    # -----------------------------------------
    # Status filter
    # -----------------------------------------

    if status_filter == "upcoming":

        query["status"] = {
            "$in": [
                "pending",
                "confirmed",
                "upcoming"
            ]
        }

    elif status_filter:

        query["status"] = status_filter

    # -----------------------------------------
    # Query appointments
    # -----------------------------------------

    cursor = appointments_collection.find(
        query
    ).sort(
        [
            ("appointment_date", -1),
            ("appointment_time", -1)
        ]
    )

    # Dashboard uses limit=5
    if limit is not None:
        cursor = cursor.limit(limit)

    return list(cursor)


def get_patient_appointment_by_id(
    patient_id,
    appointment_id
):
    """
    Get a single appointment belonging to
    the logged-in patient.
    """

    object_id = convert_to_object_id(
        appointment_id
    )

    if not object_id:
        return None

    return appointments_collection.find_one({
        "_id": object_id,
        "patient_id": str(patient_id)
    })


def cancel_patient_appointment(
    patient_id,
    appointment_id
):
    """
    Cancel an appointment belonging to the patient.
    """

    object_id = convert_to_object_id(
        appointment_id
    )

    if not object_id:
        return False

    result = appointments_collection.update_one(
        {
            "_id": object_id,
            "patient_id": str(patient_id)
        },
        {
            "$set": {
                "status": "cancelled"
            }
        }
    )

    return result.modified_count > 0


# =========================================================
# APPOINTMENT COUNTS
# =========================================================

def get_patient_appointment_count(patient_id):
    """
    Total appointments of patient.
    """

    return appointments_collection.count_documents({
        "patient_id": str(patient_id)
    })


def get_patient_upcoming_count(patient_id):
    """
    Count upcoming appointments.

    pending, confirmed and upcoming
    are considered upcoming.
    """

    return appointments_collection.count_documents({
        "patient_id": str(patient_id),
        "status": {
            "$in": [
                "pending",
                "confirmed",
                "upcoming"
            ]
        }
    })


def get_patient_completed_count(patient_id):
    """
    Count completed appointments.
    """

    return appointments_collection.count_documents({
        "patient_id": str(patient_id),
        "status": "completed"
    })


def get_patient_cancelled_count(patient_id):
    """
    Count cancelled appointments.
    """

    return appointments_collection.count_documents({
        "patient_id": str(patient_id),
        "status": "cancelled"
    })


def get_patient_appointment_counts(patient_id):
    """
    Get all appointment counts for the patient.

    Used by the Patient Appointments page.
    """

    return {
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
        )
    }


# =========================================================
# DOCTORS
# =========================================================

def get_doctor_count():
    """
    Count active doctors.
    """

    return users_collection.count_documents({
        "role": "doctor",
        "is_active": True
    })


# =========================================================
# DEPARTMENTS
# =========================================================

def get_active_department_count():
    """
    Count active departments.
    """

    return departments_collection.count_documents({
        "status": "active"
    })


# =========================================================
# UPCOMING APPOINTMENT
# =========================================================

def get_upcoming_appointment(patient_id):
    """
    Get the nearest upcoming appointment.
    """

    return appointments_collection.find_one(
        {
            "patient_id": str(patient_id),
            "status": {
                "$in": [
                    "pending",
                    "confirmed",
                    "upcoming"
                ]
            }
        },
        sort=[
            ("appointment_date", 1),
            ("appointment_time", 1)
        ]
    )


# =========================================================
# OBJECT ID HELPER
# =========================================================

def convert_to_object_id(value):
    """
    Convert string ID to MongoDB ObjectId.
    """

    try:
        return ObjectId(value)

    except (InvalidId, TypeError):
        return None





# Medical records apis 



# =========================================================
# MEDICAL RECORDS
# =========================================================

def get_patient_medical_records(patient_id, record_type=None):
    """
    Get all medical records belonging to a specific patient.
    Optional filtering by record type.
    """

    query = {
        "patient_id": str(patient_id)
    }

    if record_type:
        query["type"] = record_type

    cursor = medical_records_collection.find(query).sort(
        [
            ("date", -1),
            ("created_at", -1)
        ]
    )

    return list(cursor)


def get_patient_medical_record_by_id(patient_id, record_id):
    """
    Get a single medical record belonging to the patient.
    """

    object_id = convert_to_object_id(record_id)

    if not object_id:
        return None

    return medical_records_collection.find_one({
        "_id": object_id,
        "patient_id": str(patient_id)
    })


def get_patient_medical_record_count(patient_id):
    """
    Get total number of medical records.
    """

    return medical_records_collection.count_documents({
        "patient_id": str(patient_id)
    })


def get_patient_consultation_count(patient_id):
    """
    Get total consultation records.
    """

    return medical_records_collection.count_documents({
        "patient_id": str(patient_id),
        "type": "consultation"
    })


def get_patient_lab_report_count(patient_id):
    """
    Get total lab reports.
    """

    return medical_records_collection.count_documents({
        "patient_id": str(patient_id),
        "type": "lab_report"
    })


def get_patient_prescription_count(patient_id):
    """
    Get total prescriptions.
    """

    return medical_records_collection.count_documents({
        "patient_id": str(patient_id),
        "type": "prescription"
    })


def get_patient_medical_record_counts(patient_id):
    """
    Get all medical record summary counts.
    """

    return {
        "total": get_patient_medical_record_count(patient_id),
        "consultations": get_patient_consultation_count(patient_id),
        "lab_reports": get_patient_lab_report_count(patient_id),
        "prescriptions": get_patient_prescription_count(patient_id)
    }


# =========================================================
# OBJECT ID HELPER
# =========================================================

def convert_to_object_id(value):
    """
    Convert string ID to MongoDB ObjectId.
    """

    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None