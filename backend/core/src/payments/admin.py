from django.contrib import admin

from payments.infrastructure.db.models import Order, OrderProduct, PromoCode


class ProductInline(admin.StackedInline):
    model = OrderProduct
    readonly_fields = ('product', 'count')
    max_num = 0

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related('product')
            .only('count', 'product__title', 'product__price', 'order_id')
        )


class OrderAdmin(admin.ModelAdmin):
    base_fields = (
        'id',
        'user',
        'amount',
        'is_paid',
        'delivering',
        'created_at',
    )
    list_display = (
        *base_fields,
        'done_at',
    )
    readonly_fields = (
        *base_fields,
        'without_calling',
        'customer_email',
        'receiver_name',
        'receiver_phone_number',
        'delivery_address',
        'delivery_date',
        'delivery_time',
        'note',
        'cash',
        'promo_code',
    )
    list_display_links = ('id', 'user')
    search_fields = ('id', 'uuid', 'amount')
    list_filter = (
        'is_paid',
        'delivering',
        'created_at',
        'done_at',
        'cash',
    )
    sortable_by = ('amount',)
    inlines = [ProductInline]
    show_full_result_count = False


class OrderProductAdmin(admin.ModelAdmin):
    show_full_result_count = False


class PromoCodeAdmin(admin.ModelAdmin):
    show_full_result_count = False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
