from django.conf import settings
from django.db import models

from drf_user_activity_tracker.utils import database_log_enabled

if database_log_enabled():
    """
    Load models only if DRF_ACTIVITY_TRACKER_DATABASE is True
    """


    class ActivityLogModel(models.Model):
        user_id = models.IntegerField()
        api = models.CharField(max_length=1024, help_text='API URL')
        url_path = models.CharField(max_length=512)
        url_name = models.CharField(max_length=255)
        headers = models.TextField()
        body = models.TextField()
        method = models.CharField(max_length=10, db_index=True)
        client_ip_address = models.CharField(max_length=50)
        response = models.TextField()
        status_code = models.PositiveSmallIntegerField(help_text='Response status code', db_index=True)
        execution_time = models.DecimalField(decimal_places=5, max_digits=8,
                                             help_text='Server execution time (Not complete response time.)')
        created_time = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.api

        @property
        def event_name(self):
            if hasattr(settings, 'DRF_ACTIVITY_TRACKER_EVENT_NAME'):
                if isinstance(settings.DRF_ACTIVITY_TRACKER_EVENT_NAME, dict):
                    return settings.DRF_ACTIVITY_TRACKER_EVENT_NAME.get(self.url_name, self.url_name)
            return self.url_name

        class Meta:
            db_table = 'drf_activity_log'
            verbose_name = 'Activity Log'
            verbose_name_plural = 'Activity Logs'
