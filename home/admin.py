from django.contrib import admin # type: ignore
from django import forms
from django.utils.safestring import mark_safe
from .models import Product, FeaturedProduct, Logo, Profile, Order, OrderItem, Slider, DeliveryFeature, AboutPage, AboutHighlight, ContactPage, ContactSubmission  # Profile import করা হয়েছে

# --------------------
# Product Admin
# --------------------
class ProductAdminForm(forms.ModelForm):
    PRODUCT_TYPE_CHOICES = [
        ('Spray perfume', 'Spray perfume'),
        ('Roll Ons', 'Roll Ons'),
    ]
    PRODUCT_GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unisex', 'Unisex'),
    ]

    product_type = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES, required=False)
    product_gender = forms.ChoiceField(choices=PRODUCT_GENDER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure existing values remain selectable even if not in predefined choices
        if getattr(self, 'instance', None) and getattr(self.instance, 'pk', None):
            current_type = getattr(self.instance, 'product_type', None)
            current_gender = getattr(self.instance, 'product_gender', None)

            type_choices = list(self.PRODUCT_TYPE_CHOICES)
            gender_choices = list(self.PRODUCT_GENDER_CHOICES)

            if current_type and current_type not in dict(type_choices):
                self.fields['product_type'].choices = [(current_type, current_type)] + type_choices

            if current_gender and current_gender not in dict(gender_choices):
                self.fields['product_gender'].choices = [(current_gender, current_gender)] + gender_choices

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('is_slider',)  # Hide from admin form


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'is_sale', 'is_popular')  # removed is_slider
    list_filter = ('is_sale', 'is_popular', 'product_type', 'product_gender')  # removed is_slider
    search_fields = ('name', 'product_type', 'product_gender', 'details')

# --------------------
# FeaturedProduct Admin
# --------------------
@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('product',)
    search_fields = ('product__name',)

# --------------------
# Slider Admin
# --------------------
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'sort_order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('id',)
    ordering = ('sort_order', '-created_at')

# --------------------
# Logo Admin
# --------------------
@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')
    search_fields = ('image',)

# --------------------
# Profile Admin
# --------------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'address')
    search_fields = ('user__username', 'full_name', 'phone', 'address')



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'total_price')

    @admin.display(description="Total Price")
    def total_price(self, obj):
        price = obj.price or 0
        quantity = obj.quantity or 0
        return price * quantity


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'order_status', 'delivery_charge', 'total_price', 'created_at')
    list_filter = ('order_status', 'created_at', 'user')
    search_fields = ('user__username', 'first_name', 'last_name', 'email')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    fields = (
        'user', 'order_status',
        'first_name', 'last_name', 'email', 'phone', 'address', 'country', 'order_notes',
        'delivery_charge', 'total_price', 'created_at'
    )
    readonly_fields = ('created_at',)

# --------------------
# DeliveryFeature Admin
# --------------------
class DeliveryFeatureForm(forms.ModelForm):
    BRAND = '#b84592'
    PAGE_CHOICES = [
        ('all', 'All pages'),
        ('home', 'Home'),
        ('shop', 'Shop'),
        ('product', 'Product detail'),
        ('cart', 'Cart'),
        ('checkout', 'Checkout'),
        ('category_male', 'Male category'),
        ('category_female', 'Female category'),
        ('category_unisex', 'Unisex category'),
        ('search', 'Search results'),
        ('about', 'About'),
        ('contact', 'Contact'),
        ('profile', 'Profile'),
        ('thankyou', 'Thank you'),
    ]
    COLOR_PRESETS = [
        ('', '— Choose preset —'),
        ('brand', 'Brand (#b84592)'),
        ('black', 'Black (#111111)'),
        ('white', 'White (#ffffff)'),
        ('gray', 'Gray (#6b7280)'),
    ]

    pages = forms.MultipleChoiceField(choices=PAGE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple)
    color_preset = forms.ChoiceField(choices=COLOR_PRESETS, required=False, help_text="Pick a preset or use the color picker below.")

    class Meta:
        model = DeliveryFeature
        fields = ('title', 'description', 'icon', 'color_preset', 'icon_color', 'icon_size', 'pages', 'is_active', 'sort_order')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # color input widget
        self.fields['icon_color'].widget = forms.TextInput(attrs={'type': 'color'})
        # initialize preset based on current color
        current_color = (self.instance.icon_color or '').lower() if getattr(self.instance, 'icon_color', None) else ''
        if current_color == self.BRAND:
            self.fields['color_preset'].initial = 'brand'
        elif current_color in ('#111111', 'black'):
            self.fields['color_preset'].initial = 'black'
        elif current_color in ('#ffffff', 'white'):
            self.fields['color_preset'].initial = 'white'
        elif current_color in ('#6b7280', 'gray'):
            self.fields['color_preset'].initial = 'gray'

        # Build swatches with live preview
        swatches = [
            ('brand', self.BRAND, 'Brand'),
            ('black', '#111111', 'Black'),
            ('white', '#ffffff', 'White'),
            ('gray', '#6b7280', 'Gray'),
        ]
        swatch_html = [
            '<div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; margin:6px 0;">'
        ]
        for key, color, label in swatches:
            swatch_html.append(
                f"<button type='button' class='df-color-swatch' data-color='{color}' data-target='id_icon_color' "
                f"style=\"width:24px;height:24px;border-radius:50%;border:1px solid #d1d5db;background:{color};cursor:pointer;\" title='{label} ({color})'></button>"
            )
        # preview chip
        preview_color = current_color or '#111111'
        swatch_html.append(
            f"<span style='margin-left:8px;'>Preview:</span><span id='df-color-preview' style='display:inline-block;width:24px;height:24px;border-radius:50%;border:1px solid #d1d5db;background:{preview_color};vertical-align:middle;'></span>"
        )
        swatch_html.append('</div>')
        swatch_html.append(
            "<script>(function(){function init(){var ps=document.querySelectorAll('.df-color-swatch');var inp=document.getElementById('id_icon_color');var pv=document.getElementById('df-color-preview');if(!inp){return setTimeout(init,50);}ps.forEach(function(btn){btn.addEventListener('click',function(){var c=this.getAttribute('data-color');if(inp){inp.value=c; try{inp.dispatchEvent(new Event('input',{bubbles:true}));}catch(e){var evt=document.createEvent('HTMLEvents');evt.initEvent('input',true,false);inp.dispatchEvent(evt);} } if(pv){pv.style.backgroundColor=c;}});}); if(inp){inp.addEventListener('input',function(){ if(pv){pv.style.backgroundColor=this.value;} });}} if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',init);} else {init();}})();</script>"
        )
        self.fields['color_preset'].help_text = mark_safe('Quick presets: ' + ''.join(swatch_html))

        initial_pages = []
        raw = (self.instance.pages or '') if self.instance and self.instance.pk else ''
        if raw:
            initial_pages = [p.strip() for p in raw.split(',') if p.strip()]
        self.fields['pages'].initial = initial_pages

    def clean_pages(self):
        values = self.cleaned_data.get('pages') or []
        # If 'all' selected, store exactly 'all'
        if 'all' in values:
            return 'all'
        return ','.join(values)

    def save(self, commit=True):
        obj = super().save(commit=False)
        # Apply preset if chosen
        preset = self.cleaned_data.get('color_preset')
        if preset == 'brand':
            obj.icon_color = self.BRAND
        elif preset == 'black':
            obj.icon_color = '#111111'
        elif preset == 'white':
            obj.icon_color = '#ffffff'
        # pages
        pages_value = self.cleaned_data.get('pages')
        if isinstance(pages_value, list):
            obj.pages = 'all' if 'all' in pages_value else ','.join(pages_value)
        if commit:
            obj.save()
        return obj

@admin.register(DeliveryFeature)
class DeliveryFeatureAdmin(admin.ModelAdmin):
    form = DeliveryFeatureForm
    list_display = ('title', 'icon', 'icon_color', 'icon_size', 'is_active', 'sort_order', 'created_at')
    list_filter = ('is_active', 'icon')
    search_fields = ('title', 'description')
    ordering = ('sort_order', 'id')
    fields = ('title', 'description', 'icon', 'color_preset', 'icon_color', 'icon_size', 'pages', 'is_active', 'sort_order')

# --------------------
# About Page Admin
# --------------------
class AboutHighlightInline(admin.TabularInline):
    model = AboutHighlight
    extra = 1

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'layout', 'updated_at')
    fields = ('title', 'content', 'image', 'layout', 'button_text', 'button_url', 'bullet1', 'bullet2', 'bullet3')
    inlines = [AboutHighlightInline]

# --------------------
# Contact Page Admin
# --------------------
@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("hero_title", "updated_at", "form_enabled", "newsletter_enabled")
    fieldsets = (
        ("Hero", {"fields": ("hero_title", "hero_subtitle", "hero_image")}),
        ("Form", {"fields": ("form_enabled", "form_title", "form_subtitle", "thank_you_message")}),
        ("Office Info", {"fields": ("address", "phone", "email", "open_hours", "map_embed_url")}),
        ("Social Links", {"fields": ("social_instagram", "social_facebook", "social_tiktok", "social_pinterest")}),
        ("Newsletter", {"fields": ("newsletter_enabled", "newsletter_title", "newsletter_subtitle", "newsletter_image")}),
    )

# --------------------
# Contact Submission Admin
# --------------------
@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at")
    search_fields = ("name", "email", "phone", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    ordering = ("-created_at",)

# --------------------
# Admin site customization
# --------------------
admin.site.site_header = "zenko."
admin.site.site_title = "zenko Admin-Panel"
admin.site.index_title = "Manage zenko."
