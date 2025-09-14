# Inventory Management System

A comprehensive Django-based inventory management system following the MVC (Model-View-Controller) architecture pattern.

## Features

- **Dashboard**: Overview of inventory with key metrics and alerts
- **Item Management**: Add, edit, and track inventory items with detailed information
- **Category Management**: Organize items into categories
- **Supplier Management**: Track supplier information and relationships
- **Stock Movements**: Record stock in/out/adjustments with full audit trail
- **Low Stock Alerts**: Automatic alerts when items fall below minimum levels
- **Reports**: Generate inventory reports and analytics
- **Admin Interface**: Full Django admin interface for advanced management

## MVC Architecture

This application follows Django's MVC pattern:

- **Models** (`models.py`): Data layer with Category, Supplier, Item, StockMovement, Order, and OrderItem models
- **Views** (`views.py`): Business logic layer handling user requests and responses
- **Templates** (`templates/`): Presentation layer with responsive Bootstrap UI
- **URLs** (`urls.py`): Controller routing requests to appropriate views

## Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   cd inventory_app
   ```

2. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create sample data (optional):**
   ```bash
   python manage.py populate_sample_data
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/
   - Default admin credentials: `admin` / `admin123`
8. **Run Tests**
 ```bash
   python manage.py test inventory
   ```

## Key Models

### Item
- Core inventory item with pricing, stock levels, and relationships
- Automatic low-stock detection
- Stock value calculation
- Profit margin computation

### StockMovement
- Tracks all inventory movements (in/out/adjustments)
- Automatically updates item stock levels
- Full audit trail with user tracking

### Category & Supplier
- Organizational structures for better inventory management
- One-to-many relationships with items

## Features Implemented

- ✅ Responsive Bootstrap UI
- ✅ Search and filtering capabilities
- ✅ Pagination for large datasets
- ✅ Low stock alerts and warnings
- ✅ Stock movement tracking
- ✅ Admin interface integration
- ✅ Form validation and error handling
- ✅ Sample data generation

## Technology Stack

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5.1.3, Font Awesome 6.0
- **Database**: SQLite (development) - easily configurable for PostgreSQL/MySQL
- **Python**: 3.12+

## Project Structure

```
inventory_app/
├── inventory/                 # Django app
│   ├── models.py             # Data models (M in MVC)
│   ├── views.py              # Business logic (C in MVC)
│   ├── forms.py              # Form definitions
│   ├── admin.py              # Admin interface
│   ├── urls.py               # URL routing
│   ├── templates/            # HTML templates (V in MVC)
│   └── management/           # Custom management commands
├── inventory_project/        # Django project settings
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## Usage

1. **Dashboard**: View inventory overview and quick actions
2. **Items**: Manage inventory items with full CRUD operations
3. **Categories**: Organize items into logical groups
4. **Suppliers**: Track vendor information
5. **Stock Movements**: Record all inventory changes
6. **Reports**: Analyze inventory data and trends

## Development Notes

- The application uses Django's built-in user authentication
- All forms include CSRF protection
- Models include proper validation and constraints
- Templates are mobile-responsive
- Admin interface is fully configured for all models

## Future Enhancements

- Purchase order management
- Barcode scanning integration
- Advanced reporting and analytics
- Email notifications for low stock
- Multi-location inventory tracking
- API endpoints for mobile apps
