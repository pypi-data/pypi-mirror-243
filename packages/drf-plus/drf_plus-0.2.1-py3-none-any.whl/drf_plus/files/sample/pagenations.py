from rest_framework import pagination


class SampleCursorPagination(pagination.CursorPagination):
    """커서 페이징"""

    page_size = 20
    max_page_size = 100
    page_size_query_param = "limit"
    ordering = "-pk"
