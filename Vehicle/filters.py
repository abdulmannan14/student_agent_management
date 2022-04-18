import django_filters as filters
from .models import Checklist


class ChecklistFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="created_at__date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="created_at__date", lookup_expr="lte")
    # status = filters.CharFilter(field_name="reservation_status", lookup_expr="icontains")

    class Meta:
        model = Checklist
        exclude = ["driver"]
