from rest_framework import serializers

from drf_user_activity_tracker.models import ActivityLogModel


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLogModel
        fields = ['id', 'event_name', 'client_ip_address', 'created_time']
