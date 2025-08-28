from django.contrib import admin
from .models import Category, Supplier, Item, StockMovement, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    list_filter = ['created_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'supplier', 'quantity_in_stock',
        'minimum_stock_level', 'unit_price', 'is_low_stock', 'is_active'
    ]
    search_fields = ['name', 'sku', 'description']
    list_filter = ['category', 'supplier', 'is_active', 'unit_of_measurement', 'created_at']
    list_editable = ['quantity_in_stock', 'minimum_stock_level', 'unit_price', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'stock_value', 'profit_margin']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'sku', 'category', 'supplier')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'selling_price', 'profit_margin')
        }),
        ('Stock Management', {
            'fields': ('quantity_in_stock', 'minimum_stock_level', 'unit_of_measurement', 'stock_value')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = 'Low Stock'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['item', 'movement_type', 'quantity', 'reference', 'created_at', 'created_by']
    search_fields = ['item__name', 'item__sku', 'reference', 'notes']
    list_filter = ['movement_type', 'created_at', 'item__category']
    readonly_fields = ['created_at']
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['item', 'quantity_ordered', 'unit_price', 'quantity_received', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier', 'status', 'order_date', 'expected_delivery_date', 'total_amount']
    search_fields = ['order_number', 'supplier__name', 'notes']
    list_filter = ['status', 'order_date', 'expected_delivery_date', 'supplier']
    readonly_fields = ['order_date', 'total_amount']
    inlines = [OrderItemInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        if not obj.order_number:
            # Auto-generate order number
            import datetime
            today = datetime.date.today()
            obj.order_number = f"PO-{today.strftime('%Y%m%d')}-{Order.objects.count() + 1:03d}"
        super().save_model(request, obj, form, change)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'item', 'quantity_ordered', 'unit_price', 'quantity_received', 'subtotal']
    search_fields = ['order__order_number', 'item__name', 'item__sku']
    list_filter = ['order__status', 'order__order_date']
