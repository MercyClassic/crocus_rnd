from dataclasses import dataclass


@dataclass
class UserData:
    id: int
    phone_number: str | None = None
    name: str | None = None
