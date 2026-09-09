from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTStatelessUserAuthentication

from docs.api.profiles import staffs_schema
from profiles.permissions import IsStaff
from profiles.staff.models import Staff
from profiles.staff.serializers import StaffSerializer


@staffs_schema
class StaffViewSet(ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all().order_by("-created_at")
    permission_classes = (IsStaff,)
    authentication_classes = (JWTStatelessUserAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user_uuid=self.request.user.user_uuid)

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.localtime())
