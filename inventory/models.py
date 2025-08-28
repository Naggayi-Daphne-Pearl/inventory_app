from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Category model for organizing inventory items"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """Supplier model for tracking item suppliers"""
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(models.Model):
    """Main inventory item model"""
    UNIT_CHOICES = [
        ('pieces', 'Pieces'),
        ('kg', 'Kilograms'),
        ('liters', 'Liters'),
        ('meters', 'Meters'),
        ('boxes', 'Boxes'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    
    # Pricing
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    # Stock management
    quantity_in_stock = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=10, help_text="Alert when stock falls below this level")
    unit_of_measurement = models.CharField(max_length=20, choices=UNIT_CHOICES, default='pieces')
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    @property
    def is_low_stock(self):
        """Check if item is below minimum stock level"""
        return self.quantity_in_stock <= self.minimum_stock_level

    @property
    def stock_value(self):
        """Calculate total value of stock on hand"""
        return self.quantity_in_stock * self.unit_price

    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.unit_price > 0:
            return ((self.selling_price - self.unit_price) / self.unit_price) * 100
        return 0


class StockMovement(models.Model):
    """Track all stock movements (in/out)"""
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Stock Adjustment'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True, help_text="Reference number or note")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item.name} - {self.movement_type} ({self.quantity})"

    def save(self, *args, **kwargs):
        """Update item stock when movement is saved"""
        super().save(*args, **kwargs)
        
        # Update the item's stock quantity
        item = self.item
        if self.movement_type == 'in':
            item.quantity_in_stock += self.quantity
        elif self.movement_type == 'out':
            item.quantity_in_stock = max(0, item.quantity_in_stock - self.quantity)
        elif self.movement_type == 'adjustment':
            item.quantity_in_stock = max(0, self.quantity)
        
        item.save()


class Order(models.Model):
    """Purchase orders for restocking"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('ordered', 'Ordered'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Order {self.order_number} - {self.supplier.name}"

    @property
    def total_amount(self):
        """Calculate total order amount"""
        return sum(item.subtotal for item in self.order_items.all())


class OrderItem(models.Model):
    """Items in a purchase order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_received = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.order.order_number} - {self.item.name}"

    @property
    def subtotal(self):
        """Calculate subtotal for this order item"""
        return self.quantity_ordered * self.unit_price

    @property
    def is_fully_received(self):
        """Check if all ordered quantity has been received"""
        return self.quantity_received >= self.quantity_ordered
