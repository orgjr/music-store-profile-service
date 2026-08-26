from django.db.models.manager import Manager

from profiles.services.profile_validation import ProfileValidationService
from profiles.validators import validate_alphanumeric


class StaffManager(Manager):
    def create(
        self,
        first_name,
        last_name,
        doc,
        address,
        neighborhood,
        city,
        state,
        country,
        role,
        address_number=None,
        address_line_2=None,
        **extra_fields,
    ):

        role = validate_alphanumeric("role", role)

        admin = ProfileValidationService.validate(
            first_name=first_name,
            last_name=last_name,
            doc=doc,
            address=address,
            address_number=address_number,
            address_line_2=address_line_2,
            neighborhood=neighborhood,
            city=city,
            state=state,
            country=country,
        )

        admin = self.model(**admin, role=role, **extra_fields)
        admin.save(using=self._db)

        return admin
