from django.contrib import admin
from .models import Product, Order, SiteSettings


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'phone',
        'city',
        'payment_method',
        'total_price',
        'is_delivered',
        'created_at',
    )

    search_fields = (
        'id',
        'name',
        'phone', 
        'city', 
    )

    list_filter = (
        'is_delivered',
        'created_at',
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('shipping_cost',)