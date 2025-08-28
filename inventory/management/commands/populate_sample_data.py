from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Item, StockMovement
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate the database with sample inventory data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and components'},
            {'name': 'Office Supplies', 'description': 'Office and stationery items'},
            {'name': 'Tools & Hardware', 'description': 'Tools and hardware equipment'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Cleaning Supplies', 'description': 'Cleaning and maintenance supplies'},
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create suppliers
        suppliers_data = [
            {
                'name': 'TechCorp Electronics',
                'contact_person': 'John Smith',
                'email': 'john@techcorp.com',
                'phone': '+1-555-0123',
                'address': '123 Tech Street, Silicon Valley, CA'
            },
            {
                'name': 'Office Pro Supplies',
                'contact_person': 'Sarah Johnson',
                'email': 'sarah@officepro.com',
                'phone': '+1-555-0456',
                'address': '456 Business Ave, New York, NY'
            },
            {
                'name': 'Hardware Solutions Inc',
                'contact_person': 'Mike Wilson',
                'email': 'mike@hardwaresolutions.com',
                'phone': '+1-555-0789',
                'address': '789 Industrial Blvd, Detroit, MI'
            },
        ]

        suppliers = []
        for sup_data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                name=sup_data['name'],
                defaults=sup_data
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(f'Created supplier: {supplier.name}')

        # Create sample items
        items_data = [
            # Electronics
            {
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with USB receiver',
                'sku': 'WMOUSE001',
                'category': categories[0],  # Electronics
                'supplier': suppliers[0],   # TechCorp
                'unit_price': Decimal('25.99'),
                'selling_price': Decimal('39.99'),
                'quantity_in_stock': 45,
                'minimum_stock_level': 10,
                'unit_of_measurement': 'pieces'
            },
            {
                'name': 'USB Cable - Type C',
                'description': '6ft USB Type-C charging cable',
                'sku': 'USBC001',
                'category': categories[0],
                'supplier': suppliers[0],
                'unit_price': Decimal('8.50'),
                'selling_price': Decimal('15.99'),
                'quantity_in_stock': 120,
                'minimum_stock_level': 25,
                'unit_of_measurement': 'pieces'
            },
            {
                'name': 'Bluetooth Headphones',
                'description': 'Noise-cancelling wireless headphones',
                'sku': 'BTHEADPH001',
                'category': categories[0],
                'supplier': suppliers[0],
                'unit_price': Decimal('75.00'),
                'selling_price': Decimal('129.99'),
                'quantity_in_stock': 8,  # Low stock
                'minimum_stock_level': 15,
                'unit_of_measurement': 'pieces'
            },
            
            # Office Supplies
            {
                'name': 'A4 Copy Paper',
                'description': 'White A4 copy paper, 500 sheets per ream',
                'sku': 'PAPER001',
                'category': categories[1],  # Office Supplies
                'supplier': suppliers[1],   # Office Pro
                'unit_price': Decimal('4.99'),
                'selling_price': Decimal('7.99'),
                'quantity_in_stock': 200,
                'minimum_stock_level': 50,
                'unit_of_measurement': 'boxes'
            },
            {
                'name': 'Blue Ink Pens',
                'description': 'Ballpoint pens with blue ink, pack of 10',
                'sku': 'PENS001',
                'category': categories[1],
                'supplier': suppliers[1],
                'unit_price': Decimal('2.50'),
                'selling_price': Decimal('4.99'),
                'quantity_in_stock': 5,  # Low stock
                'minimum_stock_level': 20,
                'unit_of_measurement': 'pieces'
            },
            {
                'name': 'Desk Organizer',
                'description': 'Multi-compartment desk organizer',
                'sku': 'DESKORG001',
                'category': categories[1],
                'supplier': suppliers[1],
                'unit_price': Decimal('12.99'),
                'selling_price': Decimal('24.99'),
                'quantity_in_stock': 30,
                'minimum_stock_level': 10,
                'unit_of_measurement': 'pieces'
            },
            
            # Tools & Hardware
            {
                'name': 'Screwdriver Set',
                'description': '12-piece screwdriver set with magnetic tips',
                'sku': 'SCREWSET001',
                'category': categories[2],  # Tools & Hardware
                'supplier': suppliers[2],   # Hardware Solutions
                'unit_price': Decimal('18.50'),
                'selling_price': Decimal('32.99'),
                'quantity_in_stock': 25,
                'minimum_stock_level': 8,
                'unit_of_measurement': 'pieces'
            },
            {
                'name': 'Measuring Tape',
                'description': '25ft retractable measuring tape',
                'sku': 'TAPE001',
                'category': categories[2],
                'supplier': suppliers[2],
                'unit_price': Decimal('9.99'),
                'selling_price': Decimal('16.99'),
                'quantity_in_stock': 15,
                'minimum_stock_level': 12,
                'unit_of_measurement': 'pieces'
            },
        ]

        admin_user = User.objects.get(username='admin')
        items = []
        
        for item_data in items_data:
            item, created = Item.objects.get_or_create(
                sku=item_data['sku'],
                defaults={**item_data, 'created_by': admin_user}
            )
            items.append(item)
            if created:
                self.stdout.write(f'Created item: {item.name}')

        # Create some stock movements
        movement_data = [
            {'item': items[0], 'type': 'in', 'quantity': 50, 'reference': 'PO-001'},
            {'item': items[1], 'type': 'in', 'quantity': 100, 'reference': 'PO-002'},
            {'item': items[0], 'type': 'out', 'quantity': 5, 'reference': 'Sale-001'},
            {'item': items[2], 'type': 'out', 'quantity': 7, 'reference': 'Sale-002'},
            {'item': items[4], 'type': 'out', 'quantity': 15, 'reference': 'Sale-003'},
        ]

        for movement in movement_data:
            stock_movement = StockMovement.objects.create(
                item=movement['item'],
                movement_type=movement['type'],
                quantity=movement['quantity'],
                reference=movement['reference'],
                notes=f"Sample {movement['type']} movement",
                created_by=admin_user
            )
            self.stdout.write(f'Created stock movement: {stock_movement}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSample data created successfully!\n'
                f'Categories: {len(categories)}\n'
                f'Suppliers: {len(suppliers)}\n'
                f'Items: {len(items)}\n'
                f'Stock Movements: {len(movement_data)}\n\n'
                f'You can now access the admin panel at /admin/\n'
                f'Username: admin\n'
                f'Password: admin123\n'
            )
        )
