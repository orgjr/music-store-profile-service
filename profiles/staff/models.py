from django.db import models

from profiles.base.models import Profile
from profiles.staff.manager import StaffManager


class Staff(Profile):
    rn = models.CharField(max_length=7)
    role = models.CharField(max_length=50)

    objects = StaffManager()

    def __str__(self):
        return self.get_full_name()
