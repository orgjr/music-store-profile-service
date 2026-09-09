from rest_framework.permissions import IsAdminUser, IsAuthenticated


class IsOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return str(obj.user_uuid) == str(request.user.user_uuid)


class IsStaff(IsAdminUser): ...


class IsOwnerOrStaff(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        admin = request.user and request.user.is_staff
        if admin is False:
            owner = str(obj.user_uuid) == str(request.user.user_uuid)
            return owner
        return admin
