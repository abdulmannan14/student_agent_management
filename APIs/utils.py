from rest_framework import pagination
from rest_framework.response import Response

from limoucloud_backend import utils as lc_utils


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        data = lc_utils.success_response(data={
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
        return Response(data)


def get_paginated_response(query_set=None, request=None, serializer_class=None, page_size=10):
    paginator = CustomPagination()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(query_set, request)
    serializer = serializer_class(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
