from rest_framework import serializers

from profiles.customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
        read_only_fields = ("uuid", "user_uuid", "created_at", "updated_at")
