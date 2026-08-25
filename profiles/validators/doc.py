def validate_doc(value: str) -> str:
    if not value.isalnum():
        raise ValueError("doc only accepts letters and numbers")
    return value.strip()
