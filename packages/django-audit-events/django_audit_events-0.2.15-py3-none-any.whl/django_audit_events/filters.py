from rest_framework_filters import FilterSet, filters

from django_audit_events.models import get_audit_event_model


class AuditEventFilterSet(FilterSet):
    user = filters.NumberFilter(name="user")
    content_type = filters.NumberFilter(name="content_type")
    object_id = filters.NumberFilter(name="object_id")
    timestamp__lt = filters.DateTimeFilter(name="timestamp", lookup_expr="lt")
    timestamp__gt = filters.DateTimeFilter(name="timestamp", lookup_expr="gt")
    timestamp__lte = filters.DateTimeFilter(name="timestamp", lookup_expr="lte")
    timestamp__gte = filters.DateTimeFilter(name="timestamp", lookup_expr="gte")

    class Meta:
        model = get_audit_event_model()
        fields = ("user", "content_type", "object_id", "timestamp")
