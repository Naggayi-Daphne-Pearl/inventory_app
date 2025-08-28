from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, F
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
import json
from .models import Item, Category, Supplier, StockMovement, Order, OrderItem
from .forms import ItemForm, CategoryForm, SupplierForm, StockMovementForm, OrderForm


def dashboard(request):
    """Dashboard view with inventory overview"""
    context = {
        'total_items': Item.objects.filter(is_active=True).count(),
        'total_categories': Category.objects.count(),
        'total_suppliers': Supplier.objects.count(),
        'low_stock_items': Item.objects.filter(
            quantity_in_stock__lte=F('minimum_stock_level'),
            is_active=True
        ).count(),
        'total_stock_value': Item.objects.filter(is_active=True).aggregate(
            total=Sum(F('quantity_in_stock') * F('unit_price'))
        )['total'] or 0,
        'recent_movements': StockMovement.objects.select_related('item', 'created_by')[:10],
        'low_stock_alerts': Item.objects.filter(
            quantity_in_stock__lte=F('minimum_stock_level'),
            is_active=True
        ).select_related('category')[:5],
    }
    return render(request, 'inventory/dashboard.html', context)


def item_list(request):
    """List all inventory items with search and filter"""
    items = Item.objects.select_related('category', 'supplier').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Category filter
    category_filter = request.GET.get('category', '')
    if category_filter:
        items = items.filter(category_id=category_filter)
    
    # Stock status filter
    stock_filter = request.GET.get('stock_status', '')
    if stock_filter == 'low':
        items = items.filter(quantity_in_stock__lte=F('minimum_stock_level'))
    elif stock_filter == 'out':
        items = items.filter(quantity_in_stock=0)
    
    # Pagination
    paginator = Paginator(items, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'search_query': search_query,
        'category_filter': category_filter,
        'stock_filter': stock_filter,
    }
    return render(request, 'inventory/item_list.html', context)


def item_detail(request, item_id):
    """Display detailed view of an item"""
    item = get_object_or_404(Item, id=item_id)
    recent_movements = StockMovement.objects.filter(item=item).select_related('created_by')[:10]
    
    context = {
        'item': item,
        'recent_movements': recent_movements,
    }
    return render(request, 'inventory/item_detail.html', context)


def item_create(request):
    """Create a new inventory item"""
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            if request.user.is_authenticated:
                item.created_by = request.user
            item.save()
            messages.success(request, f'Item "{item.name}" created successfully!')
            return redirect('inventory:item_detail', item_id=item.id)
    else:
        form = ItemForm()
    
    return render(request, 'inventory/item_form.html', {
        'form': form,
        'title': 'Add New Item'
    })


def item_edit(request, item_id):
    """Edit an existing inventory item"""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Item "{item.name}" updated successfully!')
            return redirect('inventory:item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'inventory/item_form.html', {
        'form': form,
        'item': item,
        'title': 'Edit Item'
    })


def stock_movement_create(request):
    """Create a stock movement (in/out/adjustment)"""
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            if request.user.is_authenticated:
                movement.created_by = request.user
            movement.save()
            messages.success(request, 'Stock movement recorded successfully!')
            return redirect('inventory:item_detail', item_id=movement.item.id)
    else:
        form = StockMovementForm()
        # Pre-select item if provided in URL
        item_id = request.GET.get('item_id')
        if item_id:
            form.fields['item'].initial = item_id
    
    return render(request, 'inventory/stock_movement_form.html', {
        'form': form,
        'title': 'Record Stock Movement'
    })


def category_list(request):
    """List all categories"""
    categories = Category.objects.prefetch_related('items').all()
    return render(request, 'inventory/category_list.html', {'categories': categories})


def category_create(request):
    """Create a new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('inventory:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'inventory/category_form.html', {
        'form': form,
        'title': 'Add New Category'
    })


def supplier_list(request):
    """List all suppliers"""
    suppliers = Supplier.objects.prefetch_related('items').all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})


def supplier_create(request):
    """Create a new supplier"""
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier "{supplier.name}" created successfully!')
            return redirect('inventory:supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, 'inventory/supplier_form.html', {
        'form': form,
        'title': 'Add New Supplier'
    })


def reports(request):
    """Generate inventory reports"""
    # Stock value by category
    category_stock_value = Category.objects.annotate(
        total_value=Sum(F('items__quantity_in_stock') * F('items__unit_price'))
    ).filter(total_value__gt=0)
    
    # Low stock items
    low_stock_items = Item.objects.filter(
        quantity_in_stock__lte=F('minimum_stock_level'),
        is_active=True
    ).select_related('category')
    
    # Recent stock movements
    recent_movements = StockMovement.objects.select_related('item', 'created_by')[:20]
    
    context = {
        'category_stock_value': category_stock_value,
        'low_stock_items': low_stock_items,
        'recent_movements': recent_movements,
    }
    return render(request, 'inventory/reports.html', context)


@require_http_methods(["GET"])
def api_item_search(request):
    """API endpoint for item search (for AJAX autocomplete)"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'items': []})
    
    items = Item.objects.filter(
        Q(name__icontains=query) | Q(sku__icontains=query),
        is_active=True
    )[:10]
    
    items_data = [{
        'id': item.id,
        'name': item.name,
        'sku': item.sku,
        'current_stock': item.quantity_in_stock,
    } for item in items]
    
    return JsonResponse({'items': items_data})
