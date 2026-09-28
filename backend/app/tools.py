from __future__ import annotations

from datetime import date
from backend.app.school_data import (
    STUDENTS, PARENTS, TEACHERS, PRINCIPALS, ATTENDANCE_RECORDS
)


def find_student_by_name(student_name: str):
    if not student_name:
        return None
    target = student_name.strip().lower()
    for student in STUDENTS.values():
        if student["name"].lower() == target:
            return student
    return None


def get_student_attendance(role: str, user_id: str, student_id: str) -> dict:
    student = STUDENTS.get(student_id)
    if not student:
        return {"success": False, "error": "Student not found."}

    if role == "student":
        allowed = user_id == student_id
    elif role == "parent":
        parent = PARENTS.get(user_id)
        allowed = bool(parent and student_id in parent["children"])
    elif role == "teacher":
        teacher = TEACHERS.get(user_id)
        allowed = bool(teacher and student["class_name"] in teacher["classes"])
    elif role == "principal":
        allowed = user_id in PRINCIPALS
    else:
        allowed = False

    if not allowed:
        return {"success": False, "error": "You are not authorized to view this student's attendance."}

    return {
        "success": True,
        "data": {
            "student_id": student["id"],
            "student_name": student["name"],
            "class_name": student["class_name"],
            "attendance": student["attendance"],
        },
    }


def mark_student_attendance(role: str, user_id: str, student_id: str, status: str) -> dict:
    if role != "teacher":
        return {"success": False, "error": "Only teachers are authorized to mark attendance."}

    teacher = TEACHERS.get(user_id)
    student = STUDENTS.get(student_id)

    if not teacher:
        return {"success": False, "error": "Teacher account not found."}
    if not student:
        return {"success": False, "error": "Student not found."}
    if student["class_name"] not in teacher["classes"]:
        return {"success": False, "error": "You are not authorized to mark attendance for this class."}

    status = status.strip().lower()
    if status not in {"present", "absent"}:
        return {"success": False, "error": "Attendance status must be present or absent."}

    today = str(date.today())
    ATTENDANCE_RECORDS.setdefault(student_id, {})[today] = status

    return {
        "success": True,
        "data": {
            "student_id": student_id,
            "student_name": student["name"],
            "date": today,
            "status": status,
        },
    }


def get_school_attendance(role: str, user_id: str) -> dict:
    if role != "principal" or user_id not in PRINCIPALS:
        return {"success": False, "error": "Only principals are authorized to view school attendance analytics."}

    if not STUDENTS:
        return {"success": False, "error": "No student data available."}

    overall = round(sum(s["attendance"] for s in STUDENTS.values()) / len(STUDENTS), 2)
    return {
        "success": True,
        "data": {"student_count": len(STUDENTS), "overall_attendance": overall},
    }


def create_support_request(user_id: str, user_role: str, request_type: str, confirmed: bool) -> dict:
    if user_role not in {"student", "parent"}:
        return {"success": False, "error": "Only students and parents can request human support."}
    if not confirmed:
        return {
            "success": True,
            "confirmation_required": True,
            "data": {"request_type": request_type}
        }

    # In-memory mock confirmation.
    request_id = f"REQ-{user_id}-{request_type.upper()}"
    return {
        "success": True,
        "confirmed": True,
        "data": {"request_id": request_id, "request_type": request_type, "status": "submitted"},
    }
