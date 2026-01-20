from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'city', 'postal_code', 'joined_at')
    search_fields = ('user__username', 'full_name', 'phone', 'city')
    list_filter = ('city', 'joined_at')
