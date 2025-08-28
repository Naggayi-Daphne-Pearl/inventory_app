from django import forms
from .models import Item, Category, Supplier, StockMovement, Order, OrderItem


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional description'}),
        }


class SupplierForm(forms.ModelForm):
    """Form for creating and editing suppliers"""
    
    class Meta:
        model = Supplier
        fields = ['name', 'contact_person', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address'}),
        }


class ItemForm(forms.ModelForm):
    """Form for creating and editing inventory items"""
    
    class Meta:
        model = Item
        fields = [
            'name', 'description', 'sku', 'category', 'supplier',
            'unit_price', 'selling_price', 'quantity_in_stock',
            'minimum_stock_level', 'unit_of_measurement', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Item description'}),
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Stock Keeping Unit'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantity_in_stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'minimum_stock_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'unit_of_measurement': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty option for supplier
        self.fields['supplier'].empty_label = "Select a supplier (optional)"
        self.fields['category'].empty_label = "Select a category"


class StockMovementForm(forms.ModelForm):
    """Form for recording stock movements"""
    
    class Meta:
        model = StockMovement
        fields = ['item', 'movement_type', 'quantity', 'reference', 'notes']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'movement_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reference number or note'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].empty_label = "Select an item"

    def clean_quantity(self):
        """Validate stock movement quantity"""
        quantity = self.cleaned_data.get('quantity')
        movement_type = self.cleaned_data.get('movement_type')
        item = self.cleaned_data.get('item')

        if movement_type == 'out' and item:
            if quantity > item.quantity_in_stock:
                raise forms.ValidationError(
                    f"Cannot remove {quantity} items. Only {item.quantity_in_stock} available in stock."
                )
        
        return quantity


class OrderForm(forms.ModelForm):
    """Form for creating purchase orders"""
    
    class Meta:
        model = Order
        fields = ['supplier', 'expected_delivery_date', 'notes']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'expected_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Order notes'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].empty_label = "Select a supplier"


class OrderItemForm(forms.ModelForm):
    """Form for adding items to purchase orders"""
    
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity_ordered', 'unit_price']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'quantity_ordered': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        supplier = kwargs.pop('supplier', None)
        super().__init__(*args, **kwargs)
        
        if supplier:
            # Filter items by supplier if provided
            self.fields['item'].queryset = Item.objects.filter(
                supplier=supplier, is_active=True
            )
        else:
            self.fields['item'].queryset = Item.objects.filter(is_active=True)
        
        self.fields['item'].empty_label = "Select an item"


# Formset for handling multiple order items
OrderItemFormSet = forms.inlineformset_factory(
    Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True
)
