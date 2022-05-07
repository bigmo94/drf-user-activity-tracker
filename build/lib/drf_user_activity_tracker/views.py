from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_user_activity_tracker.models import ActivityLogModel
from drf_user_activity_tracker.serializers import ActivityLogSerializer
from drf_user_activity_tracker.utils import default_database


class ActivityLogViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityLogSerializer
    queryset = ActivityLogModel.objects.using(default_database()).all()

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_params = dict()
        if not self.request.user.is_superuser:
            filter_params.update({'user_id': self.request.user.id})
        return queryset.filter(**filter_params)
