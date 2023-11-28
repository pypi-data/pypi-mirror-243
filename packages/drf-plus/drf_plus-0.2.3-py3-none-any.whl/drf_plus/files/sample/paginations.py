from rest_framework import pagination


class SampleCursorPagination(pagination.CursorPagination):
    """커서 페이징"""

    page_size = 20
    max_page_size = 100
    page_size_query_param = "limit"
    ordering = "-pk"


class SampleLimitOffsetPagination(pagination.LimitOffsetPagination):
    """리미트 오프셋 페이징"""

    default_limit = 20
    max_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"
    ordering = "-pk"
