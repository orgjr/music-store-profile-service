from profiles.customer.manager import CustomerManager
from profiles.models import Profile


class Customer(Profile):
    objects = CustomerManager()

    def __str__(self):
        return self.get_full_name()
