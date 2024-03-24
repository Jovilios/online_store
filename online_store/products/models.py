from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from online_store.accounts.models import UserProfile


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("home_garden", "Home And Garden"),
        ("collectables_antiques", "Collectables And Antiques"),
        ("electronics", "Electronics"),
        ("sport_and_hobbies", "Sport and Hobbies"),
        ("fashion", "Fashion"),
        ("cars_motorcycle", "Cars And Motorcycle"),
        ("properties", "Properties"),
        ("others", "Others")
    )

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False, validators=[MinLengthValidator(10),])
    category = models.CharField(choices=CATEGORY_CHOICES, null=False, blank=False)
    date_published = models.DateTimeField(default=timezone.now)

    @property
    def formatted_date_published(self):
        return self.date_published.strftime("%d.%m.%Y")

    class Meta:
        ordering = ["-pk"]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="media/product_photos", null=True, blank=True)

