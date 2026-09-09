from rest_framework.routers import SimpleRouter

from .views import StaffViewSet

router = SimpleRouter()
router.register("staffs", StaffViewSet, basename="staffs")

urlpatterns = router.urls
