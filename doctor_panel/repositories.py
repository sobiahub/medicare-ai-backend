from datetime import datetime, timezone, date

from config.database import db
from bson import ObjectId

users_collection = db["users"]
appointments_collection = db["appointments"]
medical_records_collection = db["medical_records"]

def get_doctor_dashboard_data(doctor_id):
    appointments_collection = db["appointments"]

    doctor_id = str(doctor_id)
    today = date.today().isoformat()


    now = datetime.now(timezone.utc)

    month_start = datetime(
        now.year,
        now.month,
        1
    )

    doctor_appointments = list(
        appointments_collection.find(
            {
                "doctor_id": doctor_id
            }
        ).sort(
            [
                ("appointment_date", 1),
                ("appointment_time", 1)
            ]
        )
    )

    today_appointments = [
        appointment
        for appointment in doctor_appointments
        if str(appointment.get("appointment_date", "")) == today
    ]

    pending_appointments = [
        appointment
        for appointment in doctor_appointments
        if appointment.get("status", "").lower() == "pending"
    ]

    completed_today = [
        appointment
        for appointment in today_appointments
        if appointment.get("status", "").lower() == "completed"
    ]

    monthly_patients = set()

    for appointment in doctor_appointments:
        created_at = appointment.get("created_at")

        if created_at and isinstance(created_at, datetime):
            if created_at >= month_start:
                patient_id = appointment.get("patient_id")

                if patient_id:
                    monthly_patients.add(
                        str(patient_id)
                    )

        elif str(appointment.get("appointment_date", "")).startswith(
            now.strftime("%Y-%m")
        ):
            patient_id = appointment.get("patient_id")

            if patient_id:
                monthly_patients.add(
                    str(patient_id)
                )

    recent_patients = []
    patient_ids = set()

    for appointment in reversed(doctor_appointments):

        patient_id = appointment.get("patient_id")

        if not patient_id:
            continue

        patient_id = str(patient_id)

        if patient_id in patient_ids:
            continue

        patient_ids.add(patient_id)

        recent_patients.append({
            "patient_id": patient_id,
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
            "status": appointment.get(
                "status",
                ""
            )
        })

        if len(recent_patients) == 5:
            break

    return {
        "today_appointments": today_appointments,
        "today_schedule": today_appointments,
        "total_patients": len(monthly_patients),
        "pending_requests": len(pending_appointments),
        "completed_today": len(completed_today),
        "recent_patients": recent_patients
    }





def get_doctor_appointments(
    doctor_id,
    search=None,
    status_filter=None,
    appointment_date=None
):
    from config.database import db

    appointments_collection = db["appointments"]

    query = {
        "doctor_id": str(doctor_id)
    }

    if status_filter:
        query["status"] = status_filter.lower()

    if appointment_date:
        query["appointment_date"] = appointment_date

    appointments = list(
        appointments_collection.find(
            query
        ).sort(
            "appointment_date",
            1
        )
    )

    if search:
        search = search.lower()

        appointments = [
            appointment
            for appointment in appointments
            if search in appointment.get(
                "patient_name",
                ""
            ).lower()
            or search in appointment.get(
                "patient_email",
                ""
            ).lower()
            or search in appointment.get(
                "reason",
                ""
            ).lower()
        ]

    return appointments




def get_doctor_appointment_statistics(
    doctor_id
):

    from config.database import db

    appointments_collection = db["appointments"]

    appointments = list(
        appointments_collection.find(
            {
                "doctor_id": str(doctor_id)
            }
        )
    )

    total = len(appointments)

    confirmed = sum(
        1
        for appointment in appointments
        if appointment.get("status", "").lower()
        == "confirmed"
    )

    pending = sum(
        1
        for appointment in appointments
        if appointment.get("status", "").lower()
        == "pending"
    )

    completed = sum(
        1
        for appointment in appointments
        if appointment.get("status", "").lower()
        == "completed"
    )

    return {
        "total": total,
        "confirmed": confirmed,
        "pending": pending,
        "completed": completed
    }



def get_doctor_schedule(doctor_id):

    from config.database import db

    schedule_collection = db["doctor_schedules"]

    schedule = schedule_collection.find_one(
        {
            "doctor_id": str(doctor_id)
        }
    )

    return schedule




def update_doctor_schedule(
    doctor_id,
    schedule_data
):

    from config.database import db
    from datetime import datetime

    schedule_collection = db["doctor_schedules"]

    schedule_collection.update_one(
        {
            "doctor_id": str(doctor_id)
        },
        {
            "$set": {
                **schedule_data,
                "doctor_id": str(doctor_id),
                "updated_at": datetime.utcnow()
            }
        },
        upsert=True
    )

    return schedule_collection.find_one(
        {
            "doctor_id": str(doctor_id)
        }
    )





def create_default_doctor_schedule(
    doctor_id
):

    from config.database import db
    from datetime import datetime

    schedule_collection = db["doctor_schedules"]

    schedule = {
        "doctor_id": str(doctor_id),

        "weekly_availability": [
            {
                "day": "Monday",
                "enabled": True,
                "start_time": "09:00 AM",
                "end_time": "05:00 PM"
            },
            {
                "day": "Tuesday",
                "enabled": True,
                "start_time": "09:00 AM",
                "end_time": "05:00 PM"
            },
            {
                "day": "Wednesday",
                "enabled": True,
                "start_time": "09:00 AM",
                "end_time": "05:00 PM"
            },
            {
                "day": "Thursday",
                "enabled": True,
                "start_time": "09:00 AM",
                "end_time": "05:00 PM"
            },
            {
                "day": "Friday",
                "enabled": True,
                "start_time": "09:00 AM",
                "end_time": "05:00 PM"
            },
            {
                "day": "Saturday",
                "enabled": False,
                "start_time": "",
                "end_time": ""
            },
            {
                "day": "Sunday",
                "enabled": False,
                "start_time": "",
                "end_time": ""
            }
        ],

        "slot_duration": 30,

        "consultation_type": "Online & In-person",

        "break_start": "01:00 PM",

        "break_end": "02:00 PM",

        "max_patients_per_day": 16,

        "created_at": datetime.utcnow(),

        "updated_at": datetime.utcnow()
    }

    schedule_collection.insert_one(
        schedule
    )

    return schedule




def get_doctor_profile(doctor_id):

    return db["users"].find_one(
        {
            "_id": ObjectId(doctor_id),
            "role": "doctor"
        }
    )


def update_doctor_profile(
    doctor_id,
    data
):

    db["users"].update_one(
        {
            "_id": ObjectId(doctor_id),
            "role": "doctor"
        },
        {
            "$set": data
        }
    )

    return get_doctor_profile(
        doctor_id
    )





# DOCTOR PATIENTS
# =========================================================

def get_doctor_patient_ids(doctor_id):
    """
    Get unique patient IDs who have appointments
    with this doctor.
    """

    pipeline = [
        {
            "$match": {
                "doctor_id": str(doctor_id)
            }
        },
        {
            "$group": {
                "_id": "$patient_id"
            }
        }
    ]

    result = appointments_collection.aggregate(pipeline)

    return [
        item["_id"]
        for item in result
        if item.get("_id")
    ]


def get_doctor_patients(doctor_id, search=None):
    """
    Get all patients who have appointments
    with the logged-in doctor.
    """

    patient_ids = get_doctor_patient_ids(doctor_id)

    if not patient_ids:
        return []

    query = {
        "_id": {
            "$in": patient_ids
        },
        "role": "patient"
    }

    # Search by name or email
    if search:
        query["$or"] = [
            {
                "first_name": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "last_name": {
                    "$regex": search,
                    "$options": "i"
                }
            },
            {
                "email": {
                    "$regex": search,
                    "$options": "i"
                }
            }
        ]

    return list(
        users_collection.find(query).sort(
            [
                ("first_name", 1),
                ("last_name", 1)
            ]
        )
    )


def get_doctor_patient_by_id(doctor_id, patient_id):
    """
    Get a specific patient only if that patient
    has an appointment with this doctor.
    """

    patient = users_collection.find_one({
        "_id": patient_id,
        "role": "patient"
    })

    if not patient:
        return None

    appointment = appointments_collection.find_one({
        "doctor_id": str(doctor_id),
        "patient_id": str(patient_id)
    })

    if not appointment:
        return None

    return patient


def get_doctor_patient_appointments(
    doctor_id,
    patient_id
):
    """
    Get appointments between the doctor
    and a specific patient.
    """

    return list(
        appointments_collection.find({
            "doctor_id": str(doctor_id),
            "patient_id": str(patient_id)
        }).sort(
            [
                ("appointment_date", -1),
                ("appointment_time", -1)
            ]
        )
    )


def get_doctor_patient_count(doctor_id):
    """
    Get total unique patients for a doctor.
    """

    patient_ids = get_doctor_patient_ids(doctor_id)

    return len(patient_ids)


# =========================================================
# OBJECT ID HELPER
# =========================================================

def convert_to_object_id(value):
    """
    Convert string ID into MongoDB ObjectId.
    """

    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None




# MEDICAL RECORDS
# =========================================================

def create_medical_record(record_data):
    """
    Create a new medical record.
    """

    result = medical_records_collection.insert_one(
        record_data
    )

    return medical_records_collection.find_one({
        "_id": result.inserted_id
    })


def get_doctor_medical_records(
    doctor_id,
    record_type=None
):
    """
    Get medical records created by the doctor.
    """

    query = {
        "doctor_id": str(doctor_id)
    }

    if record_type:
        query["type"] = record_type

    return list(
        medical_records_collection.find(query).sort(
            [
                ("date", -1),
                ("created_at", -1)
            ]
        )
    )


def get_doctor_medical_record_by_id(
    doctor_id,
    record_id
):
    """
    Get a specific medical record created by
    the logged-in doctor.
    """

    object_id = convert_to_object_id(record_id)

    if not object_id:
        return None

    return medical_records_collection.find_one({
        "_id": object_id,
        "doctor_id": str(doctor_id)
    })


def update_medical_record(
    doctor_id,
    record_id,
    update_data
):
    """
    Update a medical record.
    """

    object_id = convert_to_object_id(record_id)

    if not object_id:
        return None

    result = medical_records_collection.update_one(
        {
            "_id": object_id,
            "doctor_id": str(doctor_id)
        },
        {
            "$set": update_data
        }
    )

    if result.matched_count == 0:
        return None

    return medical_records_collection.find_one({
        "_id": object_id,
        "doctor_id": str(doctor_id)
    })


def delete_medical_record(
    doctor_id,
    record_id
):
    """
    Delete a medical record.
    """

    object_id = convert_to_object_id(record_id)

    if not object_id:
        return False

    result = medical_records_collection.delete_one({
        "_id": object_id,
        "doctor_id": str(doctor_id)
    })

    return result.deleted_count > 0


# =========================================================
# PATIENT
# =========================================================

def get_patient_by_id(patient_id):
    """
    Get patient from users collection.
    """

    object_id = convert_to_object_id(patient_id)

    if not object_id:
        return None

    return users_collection.find_one({
        "_id": object_id,
        "role": "patient"
    })


# =========================================================
# DOCTOR-PATIENT RELATIONSHIP
# =========================================================

def doctor_has_patient(
    doctor_id,
    patient_id
):
    """
    Check whether the patient has an appointment
    with the doctor.
    """

    return appointments_collection.find_one({
        "doctor_id": str(doctor_id),
        "patient_id": str(patient_id)
    }) is not None


# =========================================================
# OBJECT ID
# =========================================================

def convert_to_object_id(value):

    try:
        return ObjectId(value)

    except (InvalidId, TypeError):

        return None


        