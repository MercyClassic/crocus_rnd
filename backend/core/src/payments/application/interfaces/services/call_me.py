from abc import ABC, abstractmethod


class CallMeServiceInterface(ABC):
    @abstractmethod
    def create_call_me_request(
        self,
        phone_number: str,
    ) -> None:
        raise NotImplementedError
