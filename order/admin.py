from django.contrib import admin
from .models import Order, OrderItem, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ['get_product_name', 'quantity', 'price']
    readonly_fields = ['get_product_name', 'price', 'quantity']

    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = "Product Name"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['get_phone', 'get_receipt',
                    'date_created', 'lipa_mdogo', 'outstanding_balance', 'payment_completed']
    search_fields = ['get_phone', 'get_receipt', 'date_created']
    # ordering = ['date_created']
    readonly_fields = ['get_user_name', 'get_receipt_number', "date_created"]

    fieldsets = (
        ("User & Transaction Info", {
            "fields": ("get_user_name", "get_receipt_number", "date_created", "delivered"),
        }),
    )

    def get_user_name(self, obj):
        return obj.user.username or obj.user.email
    get_user_name.short_description = "Username"

    def get_receipt_number(self, obj):
        return obj.user.transaction.receipt_number
    get_receipt_number.short_description = "Mpesa Receipt Number"

    inlines = [OrderItemInline]

    def get_phone(self, obj):
        return obj.transaction.phone_number if obj.transaction else None
    get_phone.short_description = "Phone"

    def get_receipt(self, obj):
        return obj.transaction.receipt_number if obj.transaction else None
    get_receipt.short_description = "Receipt"
