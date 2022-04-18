import django_filters as filters
from .models import Reservation


class ReservationFilter(filters.FilterSet):
    from_date = filters.DateFilter(field_name="pick_up_date", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="pick_up_date", lookup_expr="lte")
    # status = filters.CharFilter(field_name="reservation_status", lookup_expr="icontains")

    class Meta:
        model = Reservation
        exclude = ["driver"]
