from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='password')

        self.category = Category.objects.create(
            title='Test Category',
            description='Description for test category'
        )

        self.product = Product.objects.create(
            title='Test Product',
            price=100.0,
            description='Test description',
            seller=self.user,
            category=self.category
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_list.html')
        self.assertContains(response, self.product.title)

    def test_product_detail_view(self):
        response = self.client.get(reverse('products_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertContains(response, self.product.title)

    def test_product_by_category_view(self):
        response = self.client.get(reverse('products_by_category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.title)
        self.assertContains(response, self.product.title)


class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='password')

        self.product = Product.objects.create(
            title='Test Product',
            price=100.0,
            description='Test description',
            seller=self.user,
            category=None
        )

    def test_cart_view_empty(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ваша корзина пуста.')

    def test_add_to_cart_view(self):
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get('cart', {})
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)], 1)

    def test_remove_from_cart_view(self):
        self.client.post(reverse('add_to_cart', args=[self.product.id]))
        cart = self.client.session.get('cart', {})
        self.assertIn(str(self.product.id), cart)

        response = self.client.post(reverse('remove_from_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session.get('cart', {})
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_view_with_items(self):
        self.client.post(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.title)
        self.assertContains(response, '100.0')
