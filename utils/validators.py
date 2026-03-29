import re

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))

def validate_phone(phone: str) -> bool:
    if not phone:
        return True  # phone is optional
    pattern = r"^\+?[\d\s\-\(\)]{7,20}$"
    return bool(re.match(pattern, phone.strip()))

def validate_contact_payload(data: dict) -> list[str]:
    errors = []
    if not data.get("firstName", "").strip():
        errors.append("First name is required.")
    if not data.get("lastName", "").strip():
        errors.append("Last name is required.")
    if not data.get("email", "").strip():
        errors.append("Email is required.")
    elif not validate_email(data["email"]):
        errors.append("Invalid email format.")
    if not validate_phone(data.get("phone", "")):
        errors.append("Invalid phone number format.")
    allowed_categories = {"work", "personal", "family"}
    if data.get("category") and data["category"] not in allowed_categories:
        errors.append(f"Category must be one of: {', '.join(allowed_categories)}.")
    return errors
