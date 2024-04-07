from decimal import Decimal
from io import BytesIO
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from online_store.accounts.models import UserProfile
from online_store.products.models import Product
from django.utils import timezone


class ProductViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(email="test@example.com", password="Test123!")
        self.user_profile = UserProfile.objects.update(user=self.user, first_name="Test", last_name="User",
                                                       phone_number="1234567890", city="Test City",
                                                       address="Test Address")
        self.client.login(email="test@example.com", password="Test123!")

        self.product = Product.objects.create(user_profile=self.user.userprofile, name='Test Product',
                                              price=10.99, description='Test description', category='electronics',
                                              date_published=timezone.now())

    def test_add_product_requires_login(self):
        url = reverse('add_product')
        response = self.client.get(url)

        self.assertRedirects(response, f'/login/?next={url}')

    def test_product_creation(self):
        self.assertEqual(self.product.user_profile, self.user.userprofile)
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 10.99)
        self.assertEqual(self.product.description, 'Test description')
        self.assertEqual(self.product.category, 'electronics')
        self.assertIsNotNone(self.product.date_published)
        self.assertTrue(self.product.date_published <= timezone.now())

    def test_add_product_view(self):
        # Create a BytesIO buffer to simulate an image file
        image_data = BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(image_data, 'JPEG')
        image_data.seek(0)

        # Create an InMemoryUploadedFile instance
        mock_image = InMemoryUploadedFile(
            image_data,
            None,
            'test_image.jpg',
            'image/jpeg',
            len(image_data.getvalue()),
            None
        )

        self.client.force_login(self.user)
        initial_product_count = Product.objects.count()

        form_data = {
            'name': 'Test',
            'price': 10.00,
            'description': 'Test description',
            'category': 'electronics',
            'date_published': timezone.now(),
            'photos': mock_image
        }

        response = self.client.post(reverse('add_product'), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), initial_product_count + 1)
        self.assertTrue(Product.objects.filter(name='Test').exists())

    def test_edit_product_view(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse('product_edit', kwargs={'pk': self.product.pk}), data={
            'name': 'Updated Product',
            'price': 20.00,
            'description': 'Updated description',
            'category': 'fashion'
        })

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 20.00)
        self.assertEqual(self.product.description, 'Updated description')
        self.assertEqual(self.product.category, 'fashion')

    def test_unauthorized_edit_product_view(self):
        another_user = get_user_model().objects.create(email='another@example.com', password="Test123!")
        another_profile = UserProfile.objects.filter(user=another_user).update(user=another_user, first_name='Jane', last_name='Doe', phone_number='9876543210', city='Los Angeles', address='456 Street')

        self.client.force_login(another_user)

        response = self.client.post(reverse('product_edit', kwargs={'pk': self.product.pk}), data={
            'name': 'Attempted Edit',
            'price': 15.00,
            'description': 'Attempted description',
            'category': 'others'
        })

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('10.99'))
        self.assertEqual(self.product.description, 'Test description')
        self.assertEqual(self.product.category, 'electronics')

    def test_delete_product_view(self):
        self.client.force_login(self.user)

        initial_product_count = Product.objects.count()

        form_data = {
            'name': self.product.name,
            'description': self.product.description,
            'category': self.product.category,
            'price': self.product.price,
            'date_published': self.product.date_published,
        }

        response = self.client.post(reverse('product_delete', kwargs={'pk': self.product.pk}), data=form_data)

        self.assertEqual(response.status_code, 302)  # Check if redirect status
        self.assertEqual(Product.objects.count(), initial_product_count - 1)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_unauthorized_delete_product_view(self):
        another_user = get_user_model().objects.create(email='another@example.com', password="Test123!")
        another_profile = UserProfile.objects.filter(user=another_user).update(user=another_user, first_name='Jane',
                                                                               last_name='Doe', phone_number='9876543210',
                                                                               city='Los Angeles', address='456 Street')

        self.client.force_login(another_user)
        response = self.client.post(reverse('product_delete', kwargs={'pk': self.product.pk}))
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_profile_completion_redirect(self):
        another_user = get_user_model().objects.create(email='another@example.com', password="Test123!")
        self.client.force_login(another_user)

        response = self.client.get(reverse('add_product'))

        self.assertRedirects(response, reverse('profile_edit', kwargs={'pk': another_user.userprofile.pk}))
        self.assertEqual(Product.objects.count(), 1)

    def test_formatted_date_published(self):
        formatted_date = self.product.formatted_date_published
        self.assertEqual(formatted_date, self.product.date_published.strftime("%d.%m.%Y"))

