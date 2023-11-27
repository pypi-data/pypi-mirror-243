from rest_framework import views, viewsets, mixins

from drf_plus.files.sample.models import Sample


class SampleView(views.APIView):
    pass


class SampleViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Sample.objects.filter(is_deleted=False)
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = WishDrawerCursorPagination
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "wish_drawer_item"
    filterset_class = WishDrawerItemFilterSet
    ordering = "-id"
    ordering_fields = ["id", "-id"]

