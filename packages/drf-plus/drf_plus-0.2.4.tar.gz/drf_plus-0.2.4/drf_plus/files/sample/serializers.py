from rest_framework import serializers

from .models import Sample


class NestedSampleSerializer(serializers.Serializer):
    """중첩 시리얼라이저"""

    class Meta:
        model = Sample
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    """샘플 시리얼라이저"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    sample = NestedSampleSerializer(help_text="중첩 시리얼라이저")
    sample_list = NestedSampleSerializer(many=True, help_text="중첩 시리얼라이저 리스트")
    additional = serializers.SerializerMethodField(help_text="추가 필드")

    def get_additional(self, obj):
        return "추가 필드"

    def to_internal_value(self, data):
        """내부 값으로 변환"""
        return super().to_internal_value(data)

    def to_representation(self, instance):
        """표현 값으로 변환"""
        return super().to_representation(instance)

    def validate(self, attrs):
        """유효성 검사 - 전채"""
        return super().validate(attrs)

    def validate_name(self, value):
        """유효성 검사 - 필드별"""
        return super().validate_name(value)

    def save(self, **kwargs):
        """
        데이터 저장

        self.instance 가 있는 경우 update
        self.instance 가 없는 경우 create
        """
        return super().save(**kwargs)

    def create(self, validated_data):
        """생성"""
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """업데이트"""
        return super().update(instance, validated_data)

    class Meta:
        model = Sample
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "name": {"label": "이름", "help_text": "이름입니다."},
            "description": {"label": "설명", "help_text": "설명입니다."},
        }


class DoesntStoreSerializer(serializers.Serializer):
    """저장하지 않는 시리얼라이저"""

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
