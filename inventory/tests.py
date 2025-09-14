
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Supplier, Item, StockMovement
from .forms import CategoryForm, ItemForm, StockMovementForm

class CategoryModelTest(TestCase):
	def test_category_creation(self):
		category = Category.objects.create(name="Electronics", description="Electronic items")
		self.assertEqual(str(category), "Electronics")
		self.assertTrue(Category.objects.filter(name="Electronics").exists())

class SupplierModelTest(TestCase):
	def test_supplier_creation(self):
		supplier = Supplier.objects.create(name="ABC Supplies", email="abc@example.com")
		self.assertEqual(str(supplier), "ABC Supplies")

class ItemModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username="tester")
		self.category = Category.objects.create(name="Stationery")
		self.supplier = Supplier.objects.create(name="XYZ Ltd")

	def test_item_creation_and_properties(self):
		item = Item.objects.create(
			name="Pen",
			sku="PEN001",
			category=self.category,
			supplier=self.supplier,
			unit_price=10.00,
			selling_price=15.00,
			quantity_in_stock=50,
			minimum_stock_level=10,
			unit_of_measurement='pieces',
			is_active=True,
			created_by=self.user
		)
		self.assertEqual(str(item), "Pen (PEN001)")
		self.assertFalse(item.is_low_stock)
		self.assertEqual(item.stock_value, 500.00)
		self.assertAlmostEqual(item.profit_margin, 50.0)

class CategoryFormTest(TestCase):
	def test_valid_form(self):
		form = CategoryForm(data={"name": "Books", "description": "All books"})
		self.assertTrue(form.is_valid())

	def test_invalid_form(self):
		form = CategoryForm(data={"name": ""})
		self.assertFalse(form.is_valid())

class ItemFormTest(TestCase):
	def setUp(self):
		self.category = Category.objects.create(name="Food")

	def test_valid_form(self):
		form = ItemForm(data={
			"name": "Bread",
			"sku": "BRD001",
			"category": self.category.id,
			"unit_price": 2.00,
			"selling_price": 3.00,
			"quantity_in_stock": 20,
			"minimum_stock_level": 5,
			"unit_of_measurement": "pieces",
			"is_active": True
		})
		self.assertTrue(form.is_valid())

class StockMovementFormTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username="tester")
		self.category = Category.objects.create(name="Drinks")
		self.item = Item.objects.create(
			name="Soda",
			sku="SODA001",
			category=self.category,
			unit_price=1.00,
			selling_price=2.00,
			quantity_in_stock=10,
			minimum_stock_level=2,
			unit_of_measurement='pieces',
			is_active=True,
			created_by=self.user
		)

	def test_valid_stock_in(self):
		form = StockMovementForm(data={
			"item": self.item.id,
			"movement_type": "in",
			"quantity": 5,
			"reference": "Restock",
			"notes": "Added stock"
		})
		self.assertTrue(form.is_valid())

	def test_invalid_stock_out(self):
		form = StockMovementForm(data={
			"item": self.item.id,
			"movement_type": "out",
			"quantity": 20,
			"reference": "Sale",
			"notes": "Sold out"
		})
		self.assertFalse(form.is_valid())

class ItemViewTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="testuser", password="pass")
		self.category = Category.objects.create(name="Office")
		self.supplier = Supplier.objects.create(name="Office Supplies")
		self.item = Item.objects.create(
			name="Chair",
			sku="CHAIR001",
			category=self.category,
			supplier=self.supplier,
			unit_price=50.00,
			selling_price=80.00,
			quantity_in_stock=5,
			minimum_stock_level=2,
			unit_of_measurement='pieces',
			is_active=True,
			created_by=self.user
		)

	def test_item_list_view(self):
		client = Client()
		response = client.get(reverse('inventory:item_list'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Chair")

	def test_item_detail_view(self):
		client = Client()
		response = client.get(reverse('inventory:item_detail', args=[self.item.id]))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Chair")
