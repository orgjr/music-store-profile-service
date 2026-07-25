from django.urls import path

from .views import admin, customer

urlpatterns = [
    path("customer/", customer, name="customer"),
    path("admin/", admin, name="admin"),
]
