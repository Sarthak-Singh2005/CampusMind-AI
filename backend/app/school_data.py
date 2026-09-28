# Mock School ERP data for CampusMind AI.
# This simulates data normally returned by school services/APIs.

STUDENTS = {
    "S001": {"id": "S001", "name": "Rahul", "class_name": "10A", "attendance": 91.2, "parent_id": "P001"},
    "S002": {"id": "S002", "name": "Priya", "class_name": "10A", "attendance": 94.5, "parent_id": "P002"},
    "S003": {"id": "S003", "name": "Amit", "class_name": "10B", "attendance": 88.7, "parent_id": "P001"},
}

PARENTS = {
    "P001": {"id": "P001", "name": "Mr. Sharma", "children": ["S001", "S003"]},
    "P002": {"id": "P002", "name": "Mrs. Patel", "children": ["S002"]},
}

TEACHERS = {
    "T001": {"id": "T001", "name": "Mrs. Mehta", "classes": ["10A"]},
    "T002": {"id": "T002", "name": "Mr. Kumar", "classes": ["10B"]},
}

PRINCIPALS = {
    "PR001": {"id": "PR001", "name": "Dr. Singh"},
}

# Mock accounts for the prototype login.
USERS = {
    "student@example.com": {"id": "S001", "name": "Rahul", "role": "student"},
    "parent@example.com": {"id": "P001", "name": "Mr. Sharma", "role": "parent"},
    "teacher@example.com": {"id": "T001", "name": "Mrs. Mehta", "role": "teacher"},
    "principal@example.com": {"id": "PR001", "name": "Dr. Singh", "role": "principal"},
}

ATTENDANCE_RECORDS = {
    "S001": {"2026-08-20": "present"},
    "S002": {"2026-08-20": "present"},
    "S003": {"2026-08-20": "present"},
}

LANGUAGES = [
    "English", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali",
    "Gujarati", "Punjabi", "Kannada", "Malayalam", "Urdu"
]
