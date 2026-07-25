from django.urls import path

from .views import customer, staff

urlpatterns = [
    path("customer/", customer, name="customer"),
    path("staff/", staff, name="staff"),
]
