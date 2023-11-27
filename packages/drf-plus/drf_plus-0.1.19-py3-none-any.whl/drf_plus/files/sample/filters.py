import django_filters

from .models import Sample


class SampleFilterSet(django_filters.FilterSet):
    """샘플 필터"""

    name = django_filters.CharFilter(
        method="filter_name",
        abel="이름 필터"
    )
    created_at_gte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_lte = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )

    def filter_name(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

    class Meta:
        model = Sample
        fields = ["name", "created_at_gte", "created_at_lte"]
