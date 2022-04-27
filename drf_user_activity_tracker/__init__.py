import os
from drf_user_activity_tracker.events import Events

if os.environ.get('RUN_MAIN', None) != 'true':
    default_app_config = 'drf_user_activity_tracker.apps.LoggerConfig'

ACTIVITY_TRACKER_SIGNAL = Events()
