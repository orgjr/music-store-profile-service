from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, StaffViewSet

router = DefaultRouter()
router.register("customer", CustomerViewSet, basename="customer")
router.register("staff", StaffViewSet, basename="staff")

urlpatterns = [
    path("", include(router.urls)),
]
