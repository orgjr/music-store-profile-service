from django.db.models.manager import Manager

from profiles.services.profile_validation import ProfileValidationService


class AdminManager(Manager):
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
        rn,
        role,
        address_number=None,
        address_line_2=None,
        **extra_fields,
    ):

        if not str(rn).isnumeric():
            raise ValueError("rn must be numeric")
        if not all(val.isalnum() or val.isspace() for val in str(role)) is True:
            raise ValueError("role has invalids characters")

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

        admin = self.model(**admin, rn=rn, role=role, **extra_fields)
        admin.save(using=self._db)

        return admin
