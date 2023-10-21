from accounts.models import Account
from accounts.schemas import UserData


class UserRepository:
    def get_or_create_customer(
        self,
        customer_phone_number: str,
        customer_name: str,
    ) -> UserData:
        try:
            user_account = Account.objects.only('id').get(phone_number=customer_phone_number)
        except Account.DoesNotExist:
            user_account = Account.objects.create(
                phone_number=customer_phone_number,
                name=customer_name,
            )
        return UserData(id=user_account.id)
