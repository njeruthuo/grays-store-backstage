from django.contrib import admin
from .models import Image, Product, Brand, Category
from django.utils.html import format_html


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview']

    def name(self, obj):
        return obj.product.name

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" style="object-fit:cover;" />', obj.image.url)
        return "(No Image)"

    image_preview.short_description = "Preview"


class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" style="object-fit:cover;" />', obj.image.url)
        return "(No Image)"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['name', 'price', 'stocked']
