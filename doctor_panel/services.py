from .repositories import (
    get_doctor_dashboard_data,
    get_doctor_appointments,
    get_doctor_appointment_statistics,
    get_doctor_schedule,
    update_doctor_schedule,
    create_default_doctor_schedule,
    get_doctor_profile,
    update_doctor_profile,

    get_doctor_patients,
    get_doctor_patient_by_id,
    get_doctor_patient_appointments,
    get_doctor_patient_count,

     create_medical_record,
    get_doctor_medical_records,
    get_doctor_medical_record_by_id,
    update_medical_record,
    delete_medical_record,
    get_patient_by_id,
    doctor_has_patient,
)


def get_doctor_dashboard(doctor_id):

    data = get_doctor_dashboard_data(
        doctor_id
    )

    return data





def get_doctor_appointments_data(
    doctor_id,
    search=None,
    status_filter=None,
    appointment_date=None
):

    appointments = get_doctor_appointments(
        doctor_id=doctor_id,
        search=search,
        status_filter=status_filter,
        appointment_date=appointment_date
    )

    statistics = get_doctor_appointment_statistics(
        doctor_id
    )

    appointment_list = []

    for appointment in appointments:

        appointment_list.append(
            {
                "id": str(
                    appointment["_id"]
                ),

                "patient_id": str(
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

                "appointment_type":
                    appointment.get(
                        "appointment_type",
                        "General Consultation"
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
                    )
            }
        )

    return {
        "statistics": statistics,
        "appointments": appointment_list
    }





def get_doctor_schedule_data(
    doctor_id
):

    schedule = get_doctor_schedule(
        doctor_id
    )

    if not schedule:

        schedule = create_default_doctor_schedule(
            doctor_id
        )

    weekly_availability = schedule.get(
        "weekly_availability",
        []
    )

    available_days = sum(
        1
        for day in weekly_availability
        if day.get("enabled", False)
    )

    total_available_minutes = 0

    for day in weekly_availability:

        if not day.get("enabled"):
            continue

        start_time = day.get(
            "start_time"
        )

        end_time = day.get(
            "end_time"
        )

        if not start_time or not end_time:
            continue

        from datetime import datetime

        try:

            start = datetime.strptime(
                start_time,
                "%I:%M %p"
            )

            end = datetime.strptime(
                end_time,
                "%I:%M %p"
            )

            minutes = (
                end - start
            ).seconds // 60

            total_available_minutes += minutes

        except ValueError:
            continue

    slot_duration = schedule.get(
        "slot_duration",
        30
    )

    available_slots = 0

    if slot_duration > 0:

        available_slots = (
            total_available_minutes
            // slot_duration
        )

    return {
        "weekly_availability":
            weekly_availability,

        "available_days":
            available_days,

        "available_slots":
            available_slots,

        "slot_duration":
            slot_duration,

        "consultation_type":
            schedule.get(
                "consultation_type",
                "Online & In-person"
            ),

        "break_start":
            schedule.get(
                "break_start",
                ""
            ),

        "break_end":
            schedule.get(
                "break_end",
                ""
            ),

        "max_patients_per_day":
            schedule.get(
                "max_patients_per_day",
                0
            ),

        "updated_at":
            schedule.get(
                "updated_at"
            )
    }



def update_doctor_schedule_data(
    doctor_id,
    schedule_data
):

    schedule = update_doctor_schedule(
        doctor_id,
        schedule_data
    )

    return schedule



def get_doctor_profile_data(
    doctor_id
):

    doctor = get_doctor_profile(
        doctor_id
    )

    if not doctor:
        return None

    return doctor


def update_doctor_profile_data(
    doctor_id,
    data
):

    doctor = get_doctor_profile(
        doctor_id
    )

    if not doctor:
        return None

    return update_doctor_profile(
        doctor_id,
        data
    )






def serialize_doctor_patient(patient):
    """
    Convert MongoDB patient document
    into API response format.
    """

    return {
        "id": str(patient.get("_id")),

        "first_name": patient.get(
            "first_name",
            ""
        ),

        "last_name": patient.get(
            "last_name",
            ""
        ),

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

        "is_active": patient.get(
            "is_active",
            False
        ),

        "is_verified": patient.get(
            "is_verified",
            False
        ),

        "created_at": (
            patient.get("created_at").isoformat()
            if patient.get("created_at")
            else None
        ),

        "updated_at": (
            patient.get("updated_at").isoformat()
            if patient.get("updated_at")
            else None
        )
    }


# =========================================================
# SERIALIZE APPOINTMENT
# =========================================================

def serialize_doctor_patient_appointment(
    appointment
):
    """
    Convert appointment document
    into API-friendly format.
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

        "created_at": (
            appointment.get("created_at").isoformat()
            if appointment.get("created_at")
            else None
        ),

        "updated_at": (
            appointment.get("updated_at").isoformat()
            if appointment.get("updated_at")
            else None
        )
    }


# =========================================================
# GET DOCTOR PATIENTS
# =========================================================

def get_doctor_patients_data(
    doctor_id,
    search=None
):
    """
    Get patients associated with the doctor.
    """

    patients = get_doctor_patients(
        doctor_id,
        search=search
    )

    return {
        "total": get_doctor_patient_count(
            doctor_id
        ),
        "patients": [
            serialize_doctor_patient(patient)
            for patient in patients
        ]
    }


# =========================================================
# GET SINGLE PATIENT
# =========================================================

def get_doctor_patient_data(
    doctor_id,
    patient_id
):
    """
    Get a specific patient belonging
    to the logged-in doctor's patient list.
    """

    patient = get_doctor_patient_by_id(
        doctor_id,
        patient_id
    )

    if not patient:
        return None

    return serialize_doctor_patient(
        patient
    )


# =========================================================
# GET PATIENT APPOINTMENTS
# =========================================================

def get_doctor_patient_appointments_data(
    doctor_id,
    patient_id
):
    """
    Get appointment history between
    doctor and patient.
    """

    appointments = get_doctor_patient_appointments(
        doctor_id,
        patient_id
    )

    return [
        serialize_doctor_patient_appointment(
            appointment
        )
        for appointment in appointments
    ]




def serialize_medical_record(record):

    return {
        "id": str(
            record.get("_id")
        ),

        "patient_id": record.get(
            "patient_id",
            ""
        ),

        "patient_name": record.get(
            "patient_name",
            ""
        ),

        "patient_email": record.get(
            "patient_email",
            ""
        ),

        "doctor_id": record.get(
            "doctor_id",
            ""
        ),

        "doctor_name": record.get(
            "doctor_name",
            ""
        ),

        "doctor_email": record.get(
            "doctor_email",
            ""
        ),

        "type": record.get(
            "type",
            ""
        ),

        "title": record.get(
            "title",
            ""
        ),

        "description": record.get(
            "description",
            ""
        ),

        "department": record.get(
            "department",
            ""
        ),

        "specialization": record.get(
            "specialization",
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
# CREATE
# =========================================================

def create_medical_record_data(
    doctor_id,
    doctor,
    validated_data
):

    patient_id = validated_data.get(
        "patient_id"
    )

    # ---------------------------------------------
    # Check patient
    # ---------------------------------------------

    patient = get_patient_by_id(
        patient_id
    )

    if not patient:
        raise ValueError(
            "Patient not found."
        )

    # ---------------------------------------------
    # Check doctor-patient relationship
    # ---------------------------------------------

    if not doctor_has_patient(
        doctor_id,
        patient_id
    ):
        raise ValueError(
            "This patient is not associated with you."
        )

    # ---------------------------------------------
    # Patient information
    # ---------------------------------------------

    patient_name = (
        f"{patient.get('first_name', '')} "
        f"{patient.get('last_name', '')}"
    ).strip()

    # ---------------------------------------------
    # Doctor information
    # ---------------------------------------------

    doctor_name = (
        f"{doctor.get('first_name', '')} "
        f"{doctor.get('last_name', '')}"
    ).strip()

    # ---------------------------------------------
    # Record data
    # ---------------------------------------------

    record_data = {
        "patient_id": str(patient_id),

        "patient_name": patient_name,

        "patient_email": patient.get(
            "email",
            ""
        ),

        "doctor_id": str(doctor_id),

        "doctor_name": doctor_name,

        "doctor_email": doctor.get(
            "email",
            ""
        ),

        "type": validated_data.get(
            "type"
        ),

        "title": validated_data.get(
            "title"
        ),

        "description": validated_data.get(
            "description",
            ""
        ),

        "department": validated_data.get(
            "department",
            ""
        ),

        "specialization": validated_data.get(
            "specialization",
            ""
        ),

        "date": str(
            validated_data.get("date")
        ),

        "status": validated_data.get(
            "status",
            "available"
        ),

        "notes": validated_data.get(
            "notes",
            ""
        ),

        "file_name": validated_data.get(
            "file_name"
        ),

        "file_url": validated_data.get(
            "file_url"
        ),

        "created_at": datetime.utcnow(),

        "updated_at": datetime.utcnow()
    }

    record = create_medical_record(
        record_data
    )

    return serialize_medical_record(
        record
    )


# =========================================================
# GET RECORDS
# =========================================================

def get_doctor_medical_records_data(
    doctor_id,
    record_type=None
):

    records = get_doctor_medical_records(
        doctor_id,
        record_type=record_type
    )

    return [
        serialize_medical_record(record)
        for record in records
    ]


# =========================================================
# GET SINGLE RECORD
# =========================================================

def get_doctor_medical_record_data(
    doctor_id,
    record_id
):

    record = get_doctor_medical_record_by_id(
        doctor_id,
        record_id
    )

    if not record:
        return None

    return serialize_medical_record(
        record
    )


# =========================================================
# UPDATE
# =========================================================

def update_medical_record_data(
    doctor_id,
    record_id,
    validated_data
):

    # Don't allow patient_id to be changed
    update_data = dict(
        validated_data
    )

    update_data.pop(
        "patient_id",
        None
    )

    update_data["updated_at"] = datetime.utcnow()

    record = update_medical_record(
        doctor_id,
        record_id,
        update_data
    )

    if not record:
        return None

    return serialize_medical_record(
        record
    )


# =========================================================
# DELETE
# =========================================================

def delete_medical_record_data(
    doctor_id,
    record_id
):

    return delete_medical_record(
        doctor_id,
        record_id
    )