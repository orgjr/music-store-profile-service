from rest_framework.decorators import api_view
from rest_framework.response import Response

from profiles.admin.models import Admin
from profiles.customer.models import Customer


# Create your views here.
@api_view(["POST"])
def customer(request):
    a = Customer.objects.create(
        first_name="Fabrício",
        last_name="Imavov",
        doc="10258192852",
        address="rua seila 234",
        neighborhood="seila",
        city="seila",
        state="SP",
        country="BRA",
    )
    return Response({"person": a.get_full_name()})


@api_view(["POST"])
def admin(request):
    a = Admin.objects.create(
        first_name="Gerúsia",
        last_name="Ivanovich",
        doc="10251171827",
        address="rua seila 234",
        neighborhood="seila",
        city="seila",
        state="SP",
        country="BRA",
        rn="1925019",
        role="customer services",
    )
    return Response({"person": a.get_full_name()})
