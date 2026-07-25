from django.db import models

from profiles.admin.manager import AdminManager
from profiles.models import Profile


class Admin(Profile):
    rn = models.CharField(max_length=7)
    role = models.CharField(max_length=50)

    objects = AdminManager()

    def __str__(self):
        return self.get_full_name()
