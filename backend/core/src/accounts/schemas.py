from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    phone_number: str
    name: str
