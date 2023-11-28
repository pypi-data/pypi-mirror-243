from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import views, viewsets, mixins, response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle

from .filters import SampleFilterSet
from .models import Sample
from .paginations import SampleCursorPagination
from .serializers import SampleSerializer


class SampleView(views.APIView):
    """샘플 뷰"""

    permission_classes = [IsAuthenticated]
    # settings 에 설정 필요
    # REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"sample_scope": "1/sec"}}
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "sample_scope"

    def get(self, request):
        """데이터 조회"""
        return response.Response()

    def post(self, request):
        """데이터 생성"""
        return response.Response()

    def put(self, request):
        """데이터 전체 업데이트"""
        return response.Response()

    def patch(self, request):
        """데이터 부분 업데이트"""
        return response.Response()


@extend_schema_view(
    create=extend_schema(summary="데이터 등록"),
    list=extend_schema(summary="데이터 목록 조회"),
    update=extend_schema(summary="데이터 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="데이터 삭제"),
)
class SampleViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    """샘플 뷰셋"""

    queryset = Sample.objects.all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = SampleCursorPagination
    # settings 에 설정 필요
    # REST_FRAMEWORK = {"DEFAULT_THROTTLE_RATES": {"sample_scope": "1/sec"}}
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "sample_scope"
    # settings 에 설정 필요
    # REST_FRAMEWORK = {"DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"]}
    filterset_class = SampleFilterSet
    # settings 에 설정 필요
    # REST_FRAMEWORK = {"DEFAULT_FILTER_BACKENDS": ["rest_framework.filters.OrderingFilter"]}
    ordering = "-id"
    ordering_fields = ["id", "-id"]

    def get_queryset(self):
        """쿼리셋 추가 및 변경"""
        return super().get_queryset()

    def get_serializer_context(self):
        """시리얼라이저 컨텍스트 추가"""
        return super().get_serializer_context()

    def get_serializer_class(self):
        """self.action 별 시리얼라이저 선택"""
        if self.action == "create":
            pass
        return super().get_serializer_class()

    def get_object(self):
        """오브젝트 추가 및 변경"""
        return super().get_object()

    def get_permissions(self):
        """퍼미션 추가 및 변경"""
        return super().get_permissions()

    def get_throttles(self):
        """쓰로틀 추가 및 변경"""
        return super().get_throttles()

    def paginate_queryset(self, queryset):
        """페이징 쿼리셋 수정"""
        return super().paginate_queryset(queryset)

    def get_paginated_response(self, data):
        """페이징 결과 데이터 수정"""
        return super().get_paginated_response(data)

    def filter_queryset(self, queryset):
        """필터 쿼리셋 수정"""
        return super().filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        """데이터 생성"""
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """데이터 리스트 조회"""
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """데이터 상세 조회"""
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """데이터 전체 업데이트"""
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """데이터 부분 업데이트"""
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """데이터 삭제"""
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """데이터가 생성되는 시점에 추가 작업"""
        super().perform_create(serializer)

    def perform_update(self, serializer):
        """데이터가 업데이트되는 시점에 추가 작업"""
        super().perform_update(serializer)

    def perform_destroy(self, instance):
        """데이터가 삭제되는 시점에 추가 작업"""
        # ex) 삭제하지 않고 특정 컬럼만 변경
        # instance.is_deleted = True
        # instance.save()
        super().perform_destroy(instance)

    @action(detail=False, methods=["POST"])
    def additional_create(self, request, *args, **kwargs):
        """추가 액션"""
        pass

    @action(
        detail=False,
        methods=["GET"],
        url_path="additional-list",
        url_name="additional-list",
    )
    def additional_list(self, request, *args, **kwargs):
        """추가 액션"""
        pass

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[AllowAny],
        serializer_class=SampleSerializer,
    )
    def additional_detail(self, request, *args, **kwargs):
        """추가 액션"""
        pass
