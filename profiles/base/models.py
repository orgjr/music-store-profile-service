from uuid import UUID, uuid4

from django.db import models


class Profile(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    doc = models.CharField(max_length=11, unique=True)
    address = models.CharField(max_length=250)
    address_number = models.CharField(max_length=10, null=True, blank=True)
    address_line_2 = models.CharField(max_length=250, null=True, blank=True)
    neighborhood = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=2)
    country = models.CharField(max_length=3)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title()

    def save(self, *args, **kwargs):
        if not isinstance(self.uuid, UUID):
            self.uuid = uuid4()
        return super().save(*args, **kwargs)
