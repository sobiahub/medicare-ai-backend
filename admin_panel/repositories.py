from datetime import datetime, timezone, timedelta
from config.database import db
from bson import ObjectId


users_collection = db["users"]

departments_collection = db["departments"]

appointments_collection = db["appointments"]


# DOCTOR REPOSITORY


def create_doctor(doctor_data):

    result = users_collection.insert_one(
        doctor_data
    )

    return users_collection.find_one({
        "_id": result.inserted_id,
        "role": "doctor"
    })


def get_all_doctors():

    return list(
        users_collection.find({
            "role": "doctor"
        }).sort(
            "created_at",
            -1
        )
    )


def get_doctor_by_id(doctor_id):

    try:

        return users_collection.find_one({
            "_id": ObjectId(doctor_id),
            "role": "doctor"
        })

    except Exception:

        return None


def get_doctor_by_email(email):

    return users_collection.find_one({
        "email": email.lower().strip(),
        "role": "doctor"
    })


def update_doctor(
    doctor_id,
    update_data
):

    try:

        result = users_collection.update_one(
            {
                "_id": ObjectId(doctor_id),
                "role": "doctor"
            },
            {
                "$set": update_data
            }
        )

        if result.matched_count == 0:

            return None

        return get_doctor_by_id(
            doctor_id
        )

    except Exception:

        return None


def delete_doctor(doctor_id):

    try:

        result = users_collection.delete_one({
            "_id": ObjectId(doctor_id),
            "role": "doctor"
        })

        return result.deleted_count > 0

    except Exception:

        return False





def get_all_patients():

    return list(
        users_collection.find({
            "role": "patient"
        }).sort(
            "created_at",
            -1
        )
    )


def get_patient_by_id(patient_id):

    try:

        return users_collection.find_one({
            "_id": ObjectId(patient_id),
            "role": "patient"
        })

    except Exception:

        return None


def get_patient_by_email(email):

    return users_collection.find_one({
        "email": email.lower().strip(),
        "role": "patient"
    })


def update_patient(
    patient_id,
    update_data
):

    try:

        result = users_collection.update_one(
            {
                "_id": ObjectId(patient_id),
                "role": "patient"
            },
            {
                "$set": update_data
            }
        )

        if result.matched_count == 0:

            return None

        return get_patient_by_id(
            patient_id
        )

    except Exception:

        return None


def delete_patient(patient_id):

    try:

        result = users_collection.delete_one({
            "_id": ObjectId(patient_id),
            "role": "patient"
        })

        return result.deleted_count > 0

    except Exception:

        return False





# APPOINTMENT REPOSITORY
appointments_collection = db["appointments"]


def create_appointment(appointment_data):

    result = appointments_collection.insert_one(
        appointment_data
    )

    return appointments_collection.find_one({
        "_id": result.inserted_id
    })


def get_all_appointments():

    return list(
        appointments_collection.find().sort(
            "created_at",
            -1
        )
    )


def get_appointment_by_id(appointment_id):

    try:

        return appointments_collection.find_one({
            "_id": ObjectId(appointment_id)
        })

    except Exception:

        return None


def update_appointment(
    appointment_id,
    update_data
):

    try:

        result = appointments_collection.update_one(
            {
                "_id": ObjectId(appointment_id)
            },
            {
                "$set": update_data
            }
        )

        if result.matched_count == 0:

            return None

        return get_appointment_by_id(
            appointment_id
        )

    except Exception:

        return None


def delete_appointment(appointment_id):

    try:

        result = appointments_collection.delete_one({
            "_id": ObjectId(appointment_id)
        })

        return result.deleted_count > 0

    except Exception:

        return False






# DEPARTMENT REPOSITORY
departments_collection = db["departments"]


def create_department(department_data):

    result = departments_collection.insert_one(
        department_data
    )

    return departments_collection.find_one({
        "_id": result.inserted_id
    })


def get_all_departments():

    return list(
        departments_collection.find().sort(
            "created_at",
            -1
        )
    )


def get_department_by_id(department_id):

    try:

        return departments_collection.find_one({
            "_id": ObjectId(department_id)
        })

    except Exception:

        return None


def get_department_by_name(name):

    return departments_collection.find_one({
        "name": {
            "$regex": f"^{name.strip()}$",
            "$options": "i"
        }
    })


def update_department(
    department_id,
    update_data
):

    try:

        result = departments_collection.update_one(
            {
                "_id": ObjectId(department_id)
            },
            {
                "$set": update_data
            }
        )

        if result.matched_count == 0:
            return None

        return get_department_by_id(
            department_id
        )

    except Exception:

        return None


def delete_department(department_id):

    try:

        result = departments_collection.delete_one({
            "_id": ObjectId(department_id)
        })

        return result.deleted_count > 0

    except Exception:

        return False



# USERS REPOSITORY
users_collection = db["users"]


def get_all_users():

    return list(
        users_collection.find().sort(
            "created_at",
            -1
        )
    )


def get_user_by_id(user_id):

    try:

        return users_collection.find_one({
            "_id": ObjectId(user_id)
        })

    except Exception:

        return None


def update_user(
    user_id,
    update_data
):

    try:

        result = users_collection.update_one(
            {
                "_id": ObjectId(user_id)
            },
            {
                "$set": update_data
            }
        )

        if result.matched_count == 0:
            return None

        return get_user_by_id(
            user_id
        )

    except Exception:

        return None


def delete_user(user_id):

    try:

        result = users_collection.delete_one({
            "_id": ObjectId(user_id)
        })

        return result.deleted_count > 0

    except Exception:

        return False




# DASHBOARD STATISTICS REPOSITORY
def get_dashboard_statistics():

    total_users = users_collection.count_documents({})

    total_patients = users_collection.count_documents({
        "role": "patient"
    })

    total_doctors = users_collection.count_documents({
        "role": "doctor"
    })

    total_admins = users_collection.count_documents({
        "role": "admin"
    })

    active_users = users_collection.count_documents({
        "is_active": True
    })

    inactive_users = users_collection.count_documents({
        "is_active": False
    })

    total_departments = departments_collection.count_documents({})

    total_appointments = appointments_collection.count_documents({})

    pending_appointments = appointments_collection.count_documents({
        "status": "pending"
    })

    confirmed_appointments = appointments_collection.count_documents({
        "status": "confirmed"
    })

    completed_appointments = appointments_collection.count_documents({
        "status": "completed"
    })

    cancelled_appointments = appointments_collection.count_documents({
        "status": "cancelled"
    })

    return {

        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": inactive_users,
        },

        "patients": {
            "total": total_patients,
        },

        "doctors": {
            "total": total_doctors,
        },

        "admins": {
            "total": total_admins,
        },

        "departments": {
            "total": total_departments,
        },

        "appointments": {
            "total": total_appointments,
            "pending": pending_appointments,
            "confirmed": confirmed_appointments,
            "completed": completed_appointments,
            "cancelled": cancelled_appointments,
        },
    }




# RECENT APPOINTMENTS REPOSITORY
def get_recent_appointments(limit=5):

    return list(
        appointments_collection.find().sort(
            "created_at",
            -1
        ).limit(limit)
    )




# REPORT DATE RANGE
def get_period_range(period):
    """
    Returns:
        start_date
        end_date
        previous_start
        previous_end
    """

    now = datetime.now(timezone.utc)

    today = datetime(
        now.year,
        now.month,
        now.day,
        tzinfo=timezone.utc
    )

    period = period.lower().strip()

    if period == "today":

        start = today
        end = today + timedelta(days=1)

        previous_start = start - timedelta(days=1)
        previous_end = start

    elif period == "this week":

        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=7)

        previous_start = start - timedelta(days=7)
        previous_end = start

    elif period == "this month":

        start = today.replace(day=1)

        if start.month == 12:
            end = start.replace(
                year=start.year + 1,
                month=1
            )
        else:
            end = start.replace(
                month=start.month + 1
            )

        previous_end = start

        if start.month == 1:
            previous_start = start.replace(
                year=start.year - 1,
                month=12
            )
        else:
            previous_start = start.replace(
                month=start.month - 1
            )

    elif period == "last month":

        if today.month == 1:

            start = today.replace(
                year=today.year - 1,
                month=12,
                day=1
            )

        else:

            start = today.replace(
                month=today.month - 1,
                day=1
            )

        if start.month == 12:

            end = start.replace(
                year=start.year + 1,
                month=1
            )

        else:

            end = start.replace(
                month=start.month + 1
            )

        previous_end = start

        if start.month == 1:

            previous_start = start.replace(
                year=start.year - 1,
                month=12
            )

        else:

            previous_start = start.replace(
                month=start.month - 1
            )

    elif period == "this year":

        start = today.replace(
            month=1,
            day=1
        )

        end = start.replace(
            year=start.year + 1
        )

        previous_start = start.replace(
            year=start.year - 1
        )

        previous_end = start

    else:

        start = today - timedelta(days=7)
        end = today + timedelta(days=1)

        previous_start = start - timedelta(days=7)
        previous_end = start

    return (
        start,
        end,
        previous_start,
        previous_end
    )


# APPOINTMENT REPORT
def get_appointment_count(start_date, end_date):

    return appointments_collection.count_documents({
        "created_at": {
            "$gte": start_date,
            "$lt": end_date
        }
    })


def get_completed_appointment_count(
    start_date,
    end_date
):

    return appointments_collection.count_documents({
        "created_at": {
            "$gte": start_date,
            "$lt": end_date
        },
        "status": {
            "$regex": "^completed$",
            "$options": "i"
        }
    })


# PATIENT REPORT
def get_total_patients():

    return users_collection.count_documents({
        "role": "patient"
    })


def get_new_patients(
    start_date,
    end_date
):

    return users_collection.count_documents({
        "role": "patient",
        "created_at": {
            "$gte": start_date,
            "$lt": end_date
        }
    })


# DOCTOR REPORT
def get_total_doctors():

    return users_collection.count_documents({
        "role": "doctor"
    })


def get_active_doctors():

    return users_collection.count_documents({
        "role": "doctor",
        "is_active": True
    })


def get_doctor_performance(
    start_date,
    end_date
):

    doctors = list(
        users_collection.find(
            {
                "role": "doctor"
            },
            {
                "password": 0
            }
        )
    )

    reports = []

    for doctor in doctors:

        doctor_id = str(
            doctor["_id"]
        )

        appointments = appointments_collection.count_documents({
            "doctor_id": doctor_id,
            "created_at": {
                "$gte": start_date,
                "$lt": end_date
            }
        })

        completed = appointments_collection.count_documents({
            "doctor_id": doctor_id,
            "created_at": {
                "$gte": start_date,
                "$lt": end_date
            },
            "status": {
                "$regex": "^completed$",
                "$options": "i"
            }
        })

        name = (
            f"{doctor.get('first_name', '')} "
            f"{doctor.get('last_name', '')}"
        ).strip()

        reports.append({
            "name": name,
            "department": doctor.get(
                "department",
                ""
            ),
            "appointments": appointments,
            "completed": completed,
            "rating": doctor.get(
                "rating",
                0
            )
        })

    reports.sort(
        key=lambda x: x["completed"],
        reverse=True
    )

    return reports


# DEPARTMENT REPORT
def get_department_reports(
    start_date,
    end_date
):

    departments = list(
        departments_collection.find()
    )

    total_appointments = appointments_collection.count_documents({
        "created_at": {
            "$gte": start_date,
            "$lt": end_date
        }
    })

    reports = []

    for department in departments:

        department_id = str(
            department["_id"]
        )

        name = department.get(
            "name",
            "Unknown"
        )

        query = {
            "created_at": {
                "$gte": start_date,
                "$lt": end_date
            }
        }

        # Support department_id
        if department_id:

            query["department_id"] = department_id

        count = appointments_collection.count_documents(
            query
        )

        percentage = 0

        if total_appointments > 0:

            percentage = round(
                (count / total_appointments) * 100,
                2
            )

        reports.append({
            "name": name,
            "appointments": count,
            "percentage": percentage
        })

    reports.sort(
        key=lambda x: x["appointments"],
        reverse=True
    )

    return reports


# APPOINTMENT TREND
def get_appointment_trend(
    start_date,
    end_date
):

    current = start_date

    trend = []

    while current < end_date:

        next_day = current + timedelta(days=1)

        total = appointments_collection.count_documents({
            "created_at": {
                "$gte": current,
                "$lt": next_day
            }
        })

        completed = appointments_collection.count_documents({
            "created_at": {
                "$gte": current,
                "$lt": next_day
            },
            "status": {
                "$regex": "^completed$",
                "$options": "i"
            }
        })

        trend.append({
            "day": current.strftime("%a"),
            "date": current.strftime("%Y-%m-%d"),
            "total": total,
            "completed": completed
        })

        current = next_day

    return trend