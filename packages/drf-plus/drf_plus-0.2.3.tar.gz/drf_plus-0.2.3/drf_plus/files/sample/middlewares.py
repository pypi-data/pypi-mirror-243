class SampleMiddleware:
    """샘플 미들웨어"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 뷰 실행 전
        response = self.get_response(request)
        # 뷰 실행 후
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # 뷰 실행 전
        pass

    def process_exception(self, request, exception):
        # 예외 발생 시
        pass

    def process_template_response(self, request, response):
        # 템플릿 렌더링 후
        return response

    def process_response(self, request, response):
        # 뷰 실행 후
        return response

    def process_request(self, request):
        # 뷰 실행 전
        pass

    def process_resource(self, request, resource, params):
        # 뷰 실행 전
        pass
