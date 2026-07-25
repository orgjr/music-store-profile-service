from rest_framework.decorators import api_view
from rest_framework.response import Response

from profiles.customer.models import Customer
from profiles.staff.models import Staff


# Create your views here.
@api_view(["POST"])
def customer(request):
    a = Customer.objects.create(
        first_name="Marcelo",
        last_name="Felisberto",
        doc="10212345452",
        address="rua seila",
        address_number="234",
        neighborhood="seila",
        city="seila",
        state="SP",
        country="BRA",
    )
    return Response({"person": a.get_full_name()})


@api_view(["POST"])
def staff(request):
    a = Staff.objects.create(
        first_name="Claudia",
        last_name="Mourão",
        doc="10125511827",
        address="rua seila",
        address_number="234",
        neighborhood="seila",
        city="seila",
        state="SP",
        country="BRA",
        rn="1925019",
        role="customer services",
    )
    return Response({"person": a.get_full_name()})
