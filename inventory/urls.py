from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Items
    path('items/', views.item_list, name='item_list'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('items/add/', views.item_create, name='item_create'),
    path('items/<int:item_id>/edit/', views.item_edit, name='item_edit'),
    
    # Stock movements
    path('stock-movement/add/', views.stock_movement_create, name='stock_movement_create'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    
    # Suppliers
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # API endpoints
    path('api/item-search/', views.api_item_search, name='api_item_search'),
]
