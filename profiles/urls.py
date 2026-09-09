from django.urls import include, path

urlpatterns = [
    path("", include("profiles.customer.urls")),
    path("", include("profiles.staff.urls")),
]
