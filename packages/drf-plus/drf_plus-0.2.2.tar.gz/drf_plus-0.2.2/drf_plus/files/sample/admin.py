from django.contrib import admin

from .models import Sample, Product, ProductImage


admin.site.register(Sample)


class ProductImageInline(admin.TabularInline):
    """제품 이미지 관리자 페이지 정의"""

    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """제품 관리자 페이지 정의"""

    list_display = ["name", "price", "is_publish", "updated_at", "created_at"]
    inlines = [ProductImageInline]
