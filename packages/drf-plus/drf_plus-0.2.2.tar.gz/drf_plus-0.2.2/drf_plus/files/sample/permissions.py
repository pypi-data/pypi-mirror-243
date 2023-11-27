from rest_framework import permissions


class SamplePermission(permissions.BasePermission):
    """샘플 권한"""

    def has_permission(self, request, view):
        """
        권한 체크

        - actions : list, retrieve, create, update, partial_update, destroy
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        객체 권한 체크

        - actions : retrieve, update, partial_update, destroy
        """
        return True
