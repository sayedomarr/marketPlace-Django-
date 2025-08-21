from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    # list_display to show the name, code, price, in_stock, stock_quantity, created_at
    list_display = ['name', 'code', 'price', 'in_stock', 'stock_quantity', 'created_at']
    # list_filter to filter by in_stock, created_at, updated_at
    list_filter = ['in_stock', 'created_at', 'updated_at']
    # search_fields to search by name, code, description (with db_index=True for performance)
    search_fields = ['name', 'code', 'description']
    # readonly_fields to make the code, created_at, updated_at fields read-only
    readonly_fields = ['code', 'created_at', 'updated_at']
    # list_editable to allow editing the price, in_stock, stock_quantity fields directly in the list view
    list_editable = ['price', 'in_stock', 'stock_quantity']
    # ordering to order by created_at (newest first)
    ordering = ['-created_at']
    # list_per_page to limit items per page for better performance
    list_per_page = 25
    # date_hierarchy for efficient date-based filtering
    date_hierarchy = 'created_at'
    # fieldsets to group the fields logically
    fieldsets = [
        ('Basic Info', {'fields': ['name', 'code', 'description']}),
        ('Pricing & Stock', {'fields': ['price', 'in_stock', 'stock_quantity']}),
        ('Media', {'fields': ['image']}),
        ('Timestamps', {'fields': ['created_at', 'updated_at']})
    ]

admin.site.register(Product, ProductAdmin)
