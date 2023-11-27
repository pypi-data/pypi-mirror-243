from django.db import models


class Sample(models.Model):
    """샘플 모델"""

    pass


class AbstractSample(models.Model):
    """공통 필드 추상화 모델"""

    created_at = models.DateTimeField(auto_now_add=True, help_text="생성일시")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정일시")

    class Meta:
        abstract = True
