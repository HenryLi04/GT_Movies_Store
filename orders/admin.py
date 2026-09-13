from django.contrib import admin

from .models import Order, OrderItem

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "user",
        "total",
        "status",
        "created_at",
    )

    search_fields = (
        "user__username",
    )

    inlines = [
        OrderItemInLine,
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display=(
            "id",
            "order",
            "movie_name",
            "unit_price",
            "quantity",
        )
    
    search_fields = (
        "movie_name",
        "order__user__username",
    )