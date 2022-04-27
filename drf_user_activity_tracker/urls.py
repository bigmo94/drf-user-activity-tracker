from rest_framework import routers

from drf_user_activity_tracker.views import ActivityLogViewSet

app_name = "activity_log"

router = routers.SimpleRouter()
router.register('history', ActivityLogViewSet, basename="history")

urlpatterns = router.urls
