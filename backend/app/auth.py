from backend.app.school_data import USERS


def authenticate_user(email: str, selected_role: str) -> dict:
    user = USERS.get(email.strip().lower())
    if not user:
        return {"success": False, "error": "Email not found. Use a demo account."}

    if user["role"] != selected_role:
        return {"success": False, "error": "The selected role does not match this account."}

    return {"success": True, "user": user}
