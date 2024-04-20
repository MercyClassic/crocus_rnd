from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    phone_number: str | None = None
    name: str | None = None
