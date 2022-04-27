import re
from django.conf import settings

SENSITIVE_KEYS = ['password', 'token', 'access', 'refresh']
if hasattr(settings, 'DRF_ACTIVITY_TRACKER_EXCLUDE_KEYS'):
    if isinstance(settings.DRF_ACTIVITY_TRACKER_EXCLUDE_KEYS, (list, tuple)):
        SENSITIVE_KEYS.extend(settings.DRF_ACTIVITY_TRACKER_EXCLUDE_KEYS)


def get_headers(request=None):
    """
        Function:       get_headers(self, request)
        Description:    To get all the headers from request
    """
    regex = re.compile('^HTTP_')
    return dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except:
        return ''


def is_activity_tracker_enabled():
    drf_activity_tracker_database = False
    if hasattr(settings, 'DRF_ACTIVITY_TRACKER_DATABASE'):
        drf_activity_tracker_database = settings.DRF_ACTIVITY_TRACKER_DATABASE

    drf_activity_tracker_signal = False
    if hasattr(settings, 'DRF_ACTIVITY_TRACKER_SIGNAL'):
        drf_activity_tracker_signal = settings.DRF_ACTIVITY_TRACKER_SIGNAL
    return drf_activity_tracker_database or drf_activity_tracker_signal


def database_log_enabled():
    drf_activity_tracker_database = False
    if hasattr(settings, 'DRF_ACTIVITY_TRACKER_DATABASE'):
        drf_activity_tracker_database = settings.DRF_ACTIVITY_TRACKER_DATABASE
    return drf_activity_tracker_database


def default_database():
    drf_activity_default_database = 'default'
    if hasattr(settings, 'DRF_ACTIVITY_TRACKER_DEFAULT_DATABASE'):
        drf_activity_default_database = settings.DRF_ACTIVITY_TRACKER_DEFAULT_DATABASE
    return drf_activity_default_database


def mask_sensitive_data(data):
    """
    Hides sensitive keys specified in sensitive_keys settings.
    Loops recursively over nested dictionaries.
    """

    if not isinstance(data, dict):
        return data

    for key, value in data.items():
        if key in SENSITIVE_KEYS:
            data[key] = "***FILTERED***"

        if isinstance(value, dict):
            data[key] = mask_sensitive_data(data[key])

        if isinstance(value, list):
            data[key] = [mask_sensitive_data(item) for item in data[key]]

    return data
