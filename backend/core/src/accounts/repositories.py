from accounts.models import Account
from accounts.schemas import UserDTO


class UserRepository:
    def get_or_create(
        self,
        customer_phone_number: str,
        customer_name: str,
    ) -> UserDTO:
        try:
            user_account = Account.objects.only('id').get(phone_number=customer_phone_number)
        except Account.DoesNotExist:
            user_account = Account.objects.create(
                phone_number=customer_phone_number,
                name=customer_name,
            )
        return UserDTO(
            id=user_account.id,
            phone_number=user_account.phone_number,
            name=user_account.name,
        )
