from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from profiles.base.models import Profile
from profiles.staff.manager import StaffManager


class StaffId(models.IntegerField):
    validators = (MinValueValidator(1000000), MaxValueValidator(9999999))
    unique = True


class Staff(Profile):
    role = models.CharField(max_length=50)
    staff_id = StaffId()

    objects = StaffManager()

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        self.generate_staff_id()
        self.full_clean()
        super().save(*args, **kwargs)

    def generate_staff_id(self):
        # verify if is a new instance and return if not
        if not self._state.adding:
            return
        if self.staff_id and not Staff.objects.filter(staff_id=self.staff_id).exists():
            return
        staff_list = Staff.objects.order_by("-staff_id")
        last = staff_list.select_for_update().first()
        if last:
            self.staff_id = last.staff_id + 1
        else:
            self.staff_id = 1000001
