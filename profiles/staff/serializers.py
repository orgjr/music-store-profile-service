from rest_framework import serializers

from profiles.staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
        read_only_fields = ("uuid", "user_uuid", "staff_id", "created_at", "updated_at")
