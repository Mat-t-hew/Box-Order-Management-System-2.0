from django.test import TestCase
from django.urls import reverse
from .models import Box, Order, OrderItem, Coupon
from .form import CheckoutForm
from django.utils import timezone

# Create your tests here.

class BoxModelTest(TestCase):
    def test_box_creation(self):
        box = Box.objects.create(size='S', price=10.00, stock=100)
        self.assertEqual(box.size, 'S')
        self.assertEqual(box.price, 10.00)
        self.assertEqual(box.stock, 100)

class CouponModelTest(TestCase):
    def test_coupon_creation(self):cd 
        coupon = Coupon.objects.create(
            code='DISCOUNT50',
            discount_percentage=50.00,
            valid_from=timezone.now(),
            valid_to=timezone.now() + timezone.timedelta(days=10),
            active=True
        )
        self.assertTrue(coupon.is_valid())
        self.assertEqual(coupon.discount_percentage, 50.00)

class OrderModelTest(TestCase):
    def test_order_creation(self):
        box = Box.objects.create(size='M', price=20.00, stock=50)
        order = Order.objects.create(
            customer_name='John Doe',
            customer_email='john@example.com',
            date_of_collection=timezone.now().date(),
            address='1234 Elm Street',
        )
        order_item = OrderItem.objects.create(
            order=order,
            box=box,
            quantity=2
        )
        self.assertEqual(order.customer_name, 'John Doe')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 2)

# Views Test Cases
class ProductListViewTest(TestCase):
    def test_product_list_view(self):
        Box.objects.create(size='L', price=30.00, stock=200)
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/product_list.html')
        self.assertContains(response, 'L Box')

class CheckoutViewTest(TestCase):
    def test_checkout_view(self):
        Box.objects.create(size='S', price=10.00, stock=50)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/checkout.html')
        
    def test_checkout_post(self):
        box = Box.objects.create(size='S', price=10.00, stock=50)
        data = {
            'customer_name': 'Jane Doe',
            'customer_email': 'jane@example.com',
            'date_of_collection': '2025-01-01',
            'address': '123 Main Street',
            'coupon_code': '',
        }
        response = self.client.post(reverse('checkout'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect after checkout

# Forms Test Cases
class CheckoutFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'customer_name': 'John Smith',
            'customer_email': 'john.smith@example.com',
            'date_of_collection': '2025-01-01',
            'address': '5678 Oak Street',
        }
        form = CheckoutForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_form(self):
        form_data = {
            'customer_name': '',
            'customer_email': 'invalid-email',
            'date_of_collection': '',
            'address': '',
        }
        form = CheckoutForm(data=form_data)
        self.assertFalse(form.is_valid())

# Admin Panel Access Test Case
class AdminPanelTest(TestCase):
    def setUp(self):
        # Create a superuser for the admin panel
        self.user = User.objects.create_superuser('admin', 'admin@example.com', 'password')
        self.client.login(username='admin', password='password')
    
    def test_admin_access(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_add_box_in_admin(self):
        response = self.client.post('/admin/main/box/add/', {
            'size': 'L',
            'price': 25.00,
            'stock': 100,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after creating a box
