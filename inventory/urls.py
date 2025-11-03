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

    # ...for chart display...
    path('stock-by-item/', views.stock_by_item_view, name='stock_by_item'),
    path('api/stock-by-item/', views.stock_by_item_data, name='stock_by_item_data'),
    
     # adding chart page for stock value by category
    path('stock-value-by-category/', views.stock_value_by_category_view, name='stock_value_by_category'),
    path('api/stock-value-by-category/', views.stock_value_by_category_data, name='stock_value_by_category_data'),

    path('api/stock-movements-time-series/', views.stock_movements_time_series_data, 
         name='stock_movements_time_series_data'),

    path('api/price-margin-data/', 
         views.price_margin_data, 
         name='price_margin_data'),

    
]
