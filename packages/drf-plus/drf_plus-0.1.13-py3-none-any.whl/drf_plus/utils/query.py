import inspect
import time
from collections import Counter

from django.db import connection


class QueryLogger:
    """
    쿼리를 관찰하고 로깅하는 클래스

    [ 사용법 ]
    1. 데코레이터로 사용
    from drf_plus.utils.query import QueryObs

    @QueryLogger(is_print=True)
    def get(self, request, *args, **kwargs):
        ...

    2. execute_wrapper로 사용
    from django.db import connection

    ql = QueryLogger()
    with connection.execute_wrapper(ql):
        ...
    """

    def __init__(self, is_print: bool = False):
        self.is_print = is_print
        self.queries = []
        self.sql_list = []
        self.total_duration = 0

    def __call__(self, *args, **kwargs):
        """데코레이터 또는 execute_wrapper 로 사용될 경우"""
        if args and callable(args[0]):
            # 데코레이터로 사용될 경우
            return self._decorator(args[0])
        else:
            # execute_wrapper 로 사용될 경우
            return self._execute(*args, **kwargs)

    def _decorator(self, func):
        """데코레이터로 사용될 경우"""
        def inner(*args, **kwargs):
            with connection.execute_wrapper(self):
                return func(*args, **kwargs)
        return inner

    def _execute(self, execute, sql, params, many, context):
        """execute_wrapper 로 사용될 경우"""
        current_query = {"sql": sql, "params": params, "many": many}
        start = time.monotonic()
        try:
            result = execute(sql, params, many, context)
        except Exception as e:
            current_query["status"] = "error"
            current_query["exception"] = e
            raise
        else:
            current_query["status"] = "ok"
            return result
        finally:
            # 수행 시간 측정 및 로깅
            self._log_query(current_query, start)

    def _log_query(self, current_query, start):
        """쿼리 수행 시간 측정 및 로깅"""
        duration = time.monotonic() - start
        duration_ms = duration * 1000
        current_query["duration"] = duration_ms
        self.total_duration += duration_ms
        current_query["total_duration"] = self.total_duration

        self.sql_list.append(current_query["sql"])
        current_query["sql_count"] = len(self.sql_list)
        result = Counter(self.sql_list)
        for key, value in result.items():
            if value >= 2:
                current_query["duplicate_query"] = value

        if self.is_print:
            print(current_query)
        self.queries.append(current_query)

    def __enter__(self):
        """로깅 시작"""
        frame = inspect.currentframe()
        previous_frame = frame.f_back
        filename = previous_frame.f_code.co_filename
        line_no = previous_frame.f_lineno
        print(f"------------------- [ {filename}:{line_no} ] -------------------")

    def __exit__(self, exc_type, exc_value, traceback):
        """로깅 종료"""
        self._print_summary()

    def _print_summary(self):
        """쿼리 요약 정보 출력"""
        queries = sorted(self.queries, key=lambda x: x["duration"], reverse=True)
        print("▶️ 쿼리 수 : ", len(queries), "개")
        if queries:
            print("▶️ 가장 오래 걸린 쿼리 :\n", queries[0]["sql"])
            print("▶️ 중복 쿼리 수 : ", queries[0].get("duplicate_query", 0), "개")
        print("▶️ 총 소요 시간 : ", self.total_duration, "ms")
