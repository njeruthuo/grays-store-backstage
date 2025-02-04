from django.contrib import admin

# Register your models here.
from .models import Image,Brand,Category,Product

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'image']

    def name(self, obj):
        return obj.product.name

class ImageInline(admin.StackedInline):
    model = Image
    extra=1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['name','price', 'stocked']