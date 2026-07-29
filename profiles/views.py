from rest_framework.viewsets import ModelViewSet

from docs.api.profiles.customer import customer_schema
from docs.api.profiles.staff import staff_schema
from profiles.customer.models import Customer
from profiles.customer.serializers import CustomerSerializer
from profiles.staff.models import Staff
from profiles.staff.serializers import StaffSerializer


@customer_schema
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


@staff_schema
class StaffViewSet(ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
