def validate_alphanumeric(attr: str, value: str) -> str:
    if not all(pace.isalnum() or pace.isspace() for pace in value) is True:
        raise ValueError(f"{attr} has invalids characters")
    return str(value).strip()
