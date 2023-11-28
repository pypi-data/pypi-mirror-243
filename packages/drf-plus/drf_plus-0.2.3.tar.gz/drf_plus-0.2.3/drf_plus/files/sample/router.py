import threading

from django.conf import settings

# API 별 데이터베이스 라우팅
thread_local = threading.local()


def use_db_for_reads_decorator(func):
    """슬레이브 데이터베이스 라우터 - 데코레이터"""

    def func_wrapper(*args, **kwargs):
        """특정 범위 슬레이브 적용"""
        if not settings.TEST:
            setattr(thread_local, "DB_FOR_READ_ONLY", "replica")
        _func = func(*args, **kwargs)
        setattr(thread_local, "DB_FOR_READ_ONLY", None)
        return _func

    return func_wrapper


class DefaultRouter:
    """데이터베이스 라우터"""

    route_app_labels = list(set(settings.DATABASES.keys()) - {"default", "replica"})

    def db_for_read(self, model, **hints):
        """읽기에서 사용할 데이터베이스"""

        # add withdrawal routing
        if model._meta.app_label == "withdrawal":
            return "withdrawal"

        # 1. 기본 라우팅
        if model._meta.app_label in self.route_app_labels:
            return model._meta.app_label

        # 2. 특정 API만 replica 적용, 그 외 None 처리
        return getattr(thread_local, "DB_FOR_READ_ONLY", None)

    def db_for_write(self, model, **hints):
        """쓰기에서 사용할 데이터베이스"""

        # add withdrawal routing
        if model._meta.app_label == "withdrawal":
            return "withdrawal"

        # 1. 기본 라우팅
        if model._meta.app_label in self.route_app_labels:
            return model._meta.app_label

        # 2. 그 외, 다음 라우터 또는 default 로 적용
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """연결 허용 여부 확인"""

        # 1. 동일한 기본 데이터베이스 엔드포인트는 연결 허용
        default_host = settings.DATABASES.get("default", {}).get("HOST")
        replica_host = settings.DATABASES.get("replica", {}).get("HOST")
        db_list = [
            key for key, value in settings.DATABASES.items() if value.get("HOST") in [default_host, replica_host]
        ]
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True

        # 2. Host 가 동일한 경우 연결 허용
        obj1_host = settings.DATABASES.get(str(obj1._state.db), {}).get("HOST")
        obj2_host = settings.DATABASES.get(str(obj2._state.db), {}).get("HOST")
        if obj1_host is not None and obj1_host == obj2_host:
            return True

        # 3. 그 외, 다음 라우터 또는 default 로 적용
        return None
