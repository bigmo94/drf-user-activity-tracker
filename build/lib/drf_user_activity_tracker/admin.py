from datetime import timedelta

from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse

from drf_user_activity_tracker.utils import database_log_enabled

if database_log_enabled():
    from drf_user_activity_tracker.models import ActivityLogModel
    from django.utils.translation import gettext_lazy as _
    import csv


    class ExportCsvMixin:
        def export_as_csv(self, request, queryset):
            meta = self.model._meta
            field_names = [field.name for field in meta.fields]

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
            writer = csv.writer(response)

            writer.writerow(field_names)
            for obj in queryset:
                row = writer.writerow([getattr(obj, field) for field in field_names])

            return response

        export_as_csv.short_description = "Export Selected"


    class SlowAPIsFilter(admin.SimpleListFilter):
        title = _('API Performance')

        # Parameter for the filter that will be used in the URL query.
        parameter_name = 'api_performance'

        def __init__(self, request, params, model, model_admin):
            super().__init__(request, params, model, model_admin)
            if hasattr(settings, 'DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE'):
                if isinstance(settings.DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE, int):  # Making sure for integer value.
                    self._DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE = settings.DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE / 1000  # Converting to seconds.

        def lookups(self, request, model_admin):
            """
            Returns a list of tuples. The first element in each
            tuple is the coded value for the option that will
            appear in the URL query. The second element is the
            human-readable name for the option that will appear
            in the right sidebar.
            """
            slow = 'Slow'
            fast = 'Fast'
            if hasattr(settings, 'DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE'):
                slow += ', >={}ms'.format(settings.DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE)
                fast += ', <{}ms'.format(settings.DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE)

            return (
                ('slow', _(slow)),
                ('fast', _(fast)),
            )

        def queryset(self, request, queryset):
            """
            Returns the filtered queryset based on the value
            provided in the query string and retrievable via
            `self.value()`.
            """
            # to decide how to filter the queryset.
            if self.value() == 'slow':
                return queryset.filter(execution_time__gte=self._DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE)
            if self.value() == 'fast':
                return queryset.filter(execution_time__lt=self._DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE)

            return queryset


    class ActivityLogAdmin(admin.ModelAdmin, ExportCsvMixin):

        actions = ["export_as_csv"]

        def __init__(self, model, admin_site):
            super().__init__(model, admin_site)
            self._DRF_ACTIVITY_TRACKER_TIMEDELTA = 0
            if hasattr(settings, 'DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE'):
                if isinstance(settings.DRF_ACTIVITY_TRACKER_SLOW_API_ABOVE, int):  # Making sure for integer value.
                    self.list_filter += (SlowAPIsFilter,)
            if hasattr(settings, 'DRF_ACTIVITY_TRACKER_TIMEDELTA'):
                if isinstance(settings.DRF_ACTIVITY_TRACKER_TIMEDELTA, int):  # Making sure for integer value.
                    self._DRF_ACTIVITY_TRACKER_TIMEDELTA = settings.DRF_ACTIVITY_TRACKER_TIMEDELTA

        def created_time_time(self, obj):
            return (obj.created_time + timedelta(minutes=self._DRF_ACTIVITY_TRACKER_TIMEDELTA)).strftime(
                "%d %b %Y %H:%M:%S")

        created_time_time.admin_order_field = 'created_time'
        created_time_time.short_description = 'created time'

        list_per_page = 20
        list_display = ('id', 'user_id', 'api', 'method', 'status_code', 'execution_time', 'created_time_time',)
        list_filter = ('created_time', 'status_code', 'method',)
        search_fields = ('body', 'response', 'headers', 'api',)
        readonly_fields = (
            'execution_time', 'client_ip_address', 'api',
            'headers', 'body', 'method', 'response', 'status_code', 'created_time_time',
        )
        exclude = ('created_time',)


        def get_queryset(self, request):
            drf_activity_tracker_default_database = 'default'
            if hasattr(settings, 'DRF_ACTIVITY_TRACKER_DEFAULT_DATABASE'):
                drf_activity_tracker_default_database = settings.DRF_ACTIVITY_TRACKER_DEFAULT_DATABASE
            return super(ActivityLogAdmin, self).get_queryset(request).using(drf_activity_tracker_default_database)


        def has_add_permission(self, request, obj=None):
            return False

        def has_change_permission(self, request, obj=None):
            return False


    admin.site.register(ActivityLogModel, ActivityLogAdmin)
