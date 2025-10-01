from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()

# ------- User Profile Model --------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# ✅ Automatically create or update Profile when User is created/updated
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile for new user
        Profile.objects.create(user=instance)
    else:
        # Only save if profile exists
        if hasattr(instance, 'profile'):
            instance.profile.save()


# --------------------
# Main Product Model
# --------------------
class Product(models.Model):
    name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200, blank=True, null=True)
    product_gender = models.CharField(max_length=200, null=True)
    new_product = models.BooleanField(default=False)
    details = models.TextField(blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # Optional fragrance notes
    top_note = models.CharField(max_length=200, blank=True, null=True)
    middle_note = models.CharField(max_length=200, blank=True, null=True)
    base_note = models.CharField(max_length=200, blank=True, null=True)
    top_note_strength = models.PositiveSmallIntegerField(default=0, help_text="0-100")
    middle_note_strength = models.PositiveSmallIntegerField(default=0, help_text="0-100")
    base_note_strength = models.PositiveSmallIntegerField(default=0, help_text="0-100")

    is_sale = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    sale_price = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    is_slider = models.BooleanField(default=False)

    image1 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image5 = models.ImageField(upload_to='product_images', blank=True, null=True)
    image6 = models.ImageField(upload_to='product_images', blank=True, null=True)

    video = models.FileField(upload_to='videos_uploaded/%y', blank=True, null=True)

    def __str__(self):
        return self.name


# --------------------
# Featured Product
# --------------------
class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Featured: {self.product.name}"


# --------------------
# Slider Model (separate from Products)
# --------------------
class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images')
    link_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return f"Slider #{self.id}"


# --------------------
# Logo Model
# --------------------
class Logo(models.Model):
    image = models.ImageField(upload_to='logo_images', blank=True, null=True)

    def __str__(self):
        return f"Logo {self.id}"

# --------------------
# Delivery Feature (dynamic delivery section)
# --------------------
class DeliveryFeature(models.Model):
    ICON_CHOICES = (
        ("truck", "Truck (Delivery)"),
        ("shield", "Shield (Cash on Delivery)"),
        ("return", "Return Arrow"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="truck")
    icon_color = models.CharField(max_length=20, default="#111111", help_text="CSS color, e.g., #111111 or 'black'")
    icon_size = models.PositiveIntegerField(default=24, help_text="Icon size in pixels")
    # Comma-separated page keys where this feature should appear. Leave blank for all pages.
    pages = models.CharField(max_length=200, blank=True, null=True, help_text="Comma-separated: all, home, shop, product, cart, checkout, category_male, category_female, category_unisex, search, about, contact, profile, thankyou")
    # Deprecated: kept for backward compat, no longer used in templates
    icon_html = models.TextField(blank=True, null=True, help_text="Deprecated. Use icon picker above.")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title

# --------------------
# About Page (dynamic content)
# --------------------
class AboutPage(models.Model):
    LAYOUT_CHOICES = (
        ('image_right', 'Image Right'),
        ('image_left', 'Image Left'),
    )
    title = models.CharField(max_length=150, default="Why Choose Us")
    content = CKEditor5Field('Text', config_name='extends', blank=True, null=True)
    # legacy bullets retained
    bullet1 = models.CharField(max_length=120, blank=True, null=True)
    bullet2 = models.CharField(max_length=120, blank=True, null=True)
    bullet3 = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to='about_images', blank=True, null=True)
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_url = models.CharField(max_length=200, default="/shop/view/")
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='image_right')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"About Page (updated {self.updated_at:%Y-%m-%d})"

class AboutHighlight(models.Model):
    about = models.ForeignKey(AboutPage, related_name='highlights', on_delete=models.CASCADE)
    text = CKEditor5Field('Text', config_name='extends')
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f"Highlight #{self.id}"


# --------------------
# Contact Page (dynamic content)
# --------------------
class ContactPage(models.Model):
    # Hero
    hero_title = models.CharField(max_length=120, default="Contact Us")
    hero_subtitle = models.CharField(max_length=200, blank=True, null=True, default="We’d love to hear from you")
    hero_image = models.ImageField(upload_to='contact_images', blank=True, null=True)

    # Form section
    form_enabled = models.BooleanField(default=True)
    form_title = models.CharField(max_length=120, default="Send us a Message")
    form_subtitle = models.CharField(max_length=200, blank=True, null=True, default="Our team will get back to you shortly.")
    thank_you_message = models.TextField(blank=True, null=True, default="Thanks for contacting us! We’ll reach out soon.")

    # Office info
    address = models.CharField(max_length=255, blank=True, null=True, default="H-31, Road 4, Block F, Sector 2, Aftabnagar, Dhaka, Bangladesh.")
    phone = models.CharField(max_length=50, blank=True, null=True, default="+880 1336046969")
    email = models.EmailField(blank=True, null=True, default="zenkobangladesh@gmail.com")
    open_hours = models.CharField(max_length=120, blank=True, null=True, default="Sunday – Friday, 10:00 AM – 5:00 PM")
    map_embed_url = models.URLField(blank=True, null=True, help_text="Use a Google Maps embed URL")

    # Social links
    social_instagram = models.URLField(blank=True, null=True)
    social_facebook = models.URLField(blank=True, null=True)
    social_tiktok = models.URLField(blank=True, null=True)
    social_pinterest = models.URLField(blank=True, null=True)

    # Newsletter
    newsletter_enabled = models.BooleanField(default=True)
    newsletter_title = models.CharField(max_length=120, default="Stay in the Aroma")
    newsletter_subtitle = models.CharField(max_length=200, blank=True, null=True, default="Join our newsletter for exclusive launches and offers.")
    newsletter_image = models.ImageField(upload_to='contact_images', blank=True, null=True, help_text="Optional background image")

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contact Page (updated {self.updated_at:%Y-%m-%d})"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=150, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject or 'Message'}"


# ------ Cart Model ---------
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    VOLUME_CHOICES = (
        ("50 ml", "50 ml"),
        ("30 ml", "30 ml"),
        ("10 ml combo", "10 ml combo"),
    )
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    volume_option = models.CharField(max_length=20, choices=VOLUME_CHOICES, default="50 ml")

    def total_price(self):
        return self.product.price * self.quantity


# ------ Order Model ------
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    order_notes = models.TextField(blank=True, null=True)

    ORDER_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    )
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="pending")

    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # New field
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)      # Subtotal + Delivery

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    VOLUME_CHOICES = (
        ("50 ml", "50 ml"),
        ("30 ml", "30 ml"),
        ("10 ml combo", "10 ml combo"),
    )
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    volume_option = models.CharField(max_length=20, choices=VOLUME_CHOICES, default="50 ml")

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
