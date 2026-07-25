from profiles.base.models import Profile
from profiles.customer.manager import CustomerManager


class Customer(Profile):
    objects = CustomerManager()

    def __str__(self):
        return self.get_full_name()
