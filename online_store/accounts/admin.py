from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin
from online_store.accounts.models import CustomUser, UserProfile
from online_store.products.models import Product, ProductImage


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "is_staff", "is_active", "is_superuser", "display_groups")
    list_filter = ("is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("groups",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active", "is_superuser")}
        ),
    )
    search_fields = ("email",)
    ordering = ("-pk",)

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    display_groups.short_description = "Groups"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "last_name", "phone_number", "city", "address")
    list_filter = ("city",)
    search_fields = ("first_name", "last_name", "user", "phone_number")
    ordering = ("-pk",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "user_profile_email", "category", "formatted_date_published")
    list_filter = ("category",)

    def user_profile_email(self, obj):
        return obj.user_profile.user.email

    user_profile_email.short_description = "User Email"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product_name", "image_tag")

    def product_name(self, obj):
        return obj.product.name

    product_name.short_description = "Product Name"

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />'.format(obj.image.url))
        else:
            return "No Image"

    image_tag.short_description = "Image Preview"

