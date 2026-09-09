from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from docs.api.profiles import customers_schema
from profiles.customer.models import Customer
from profiles.customer.serializers import CustomerSerializer
from profiles.permissions import IsOwnerOrStaff, IsStaff


@customers_schema
class CustomerViewSet(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all().order_by("-created_at")
    authentication_classes = (JWTStatelessUserAuthentication,)

    def get_permissions(self):
        if self.action in ["list", "destroy"]:
            return [IsStaff()]
        if self.action == "create":
            return [IsAuthenticated()]
        return [IsOwnerOrStaff()]

    def perform_create(self, serializer):
        serializer.save(user_uuid=self.request.user.user_uuid)

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.localtime())
