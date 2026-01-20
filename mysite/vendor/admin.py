from django.contrib import admin
from .models import Vendor, Sale        # Vendor & Sale are in vendor app
from products.models import Product     # Product is in products app


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'vendor_id', 'created_at')
    search_fields = ('shop_name', 'user__username')
    list_filter = ('created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'vendor', 'category')
    search_fields = ('product_name',)
    list_filter = ('category', 'vendor')


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'vendor', 'buyer', 'quantity', 'total_price', 'status', 'sale_date')
    list_filter = ('status', 'sale_date')
    search_fields = ('product__product_name', 'vendor__shop_name', 'buyer__username')
