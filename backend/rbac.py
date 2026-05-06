# rbac.py

# based on metadata.txt — defines which folders each role can access

ROLE_ACCESS = {
    "finance":     ["finance", "general"],
    "hr":          ["hr", "general"],
    "marketing":   ["marketing", "general"],
    "engineering": ["engineering", "general"],
    "c_level":     ["finance", "hr", "marketing", "engineering", "general"],
    "employee":    ["general"],
}

###valid roles
VALID_ROLES = list(ROLE_ACCESS.keys())


def get_allowed_roles(role: str) -> list:
    role = role.lower().strip()
    if role not in ROLE_ACCESS:
        raise ValueError(f"Unknown role: {role}")
    return ROLE_ACCESS[role]

def has_access(role: str, folder: str) -> bool:
    try:
        allowed = get_allowed_roles(role)
        return folder in allowed
    except ValueError:
        return False