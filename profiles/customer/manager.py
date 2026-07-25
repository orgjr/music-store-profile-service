from django.db.models.manager import Manager

from profiles.services.profile_validation import ProfileValidationService


class CustomerManager(Manager):
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
        address_number=None,
        address_line_2=None,
        **extra_fields,
    ):
        person = ProfileValidationService.validate(
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

        person = self.model(**person, **extra_fields)
        person.save(using=self._db)

        return person
