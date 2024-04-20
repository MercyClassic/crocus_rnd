import re


def phone_validator(value: str) -> str | None:
    phone = re.fullmatch(
        r'\+?[7, 8]-?\s*-?\(?\d{3}\)?-?\s*-?\d{3}-?\s*-?\d{2}-?\s*-?\d{2}',
        value,
        flags=re.ASCII,
    )
    return phone
