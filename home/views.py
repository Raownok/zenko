from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from decimal import Decimal
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q, Sum, F, FloatField, ExpressionWrapper, Case, When, Value
from django.db.models.functions import Coalesce
import os

# Import all needed models
from .models import (
    Product, FeaturedProduct, Logo, Cart, CartItem,
    Order, OrderItem, Profile, Slider
)

# Import forms
from .forms import UserUpdateForm, ProfileUpdateForm, CheckoutForm

# ---------------------------
# Home, Shop, and Product Views
# ---------------------------
def searchResult(request):
    # Accept both POST (from header form) and GET (pagination / direct link)
    searched = (request.POST.get('searched') or request.GET.get('q') or '').strip()
    context = { 'searched': searched }

    if searched:
        sort = request.GET.get('sort', 'new')
        qs = Product.objects.filter(
            Q(name__icontains=searched) |
            Q(product_type__icontains=searched) |
            Q(product_gender__icontains=searched) |
            Q(details__icontains=searched)
        )
        if sort == 'price_asc':
            qs = qs.order_by('price')
        elif sort == 'price_desc':
            qs = qs.order_by('-price')
        elif sort == 'name_az':
            qs = qs.order_by('name')
        elif sort == 'name_za':
            qs = qs.order_by('-name')
        elif sort == 'popular':
            qs = qs.annotate(total_sold=Coalesce(Sum('orderitem__quantity'), 0)).order_by('-total_sold', '-id')
        elif sort == 'sale':
            qs = qs.filter(is_sale=True).annotate(
                discount_perc=Case(
                    When(price__gt=0, then=ExpressionWrapper((F('price') - F('sale_price')) * Value(100.0) / F('price'), output_field=FloatField())),
                    default=Value(0.0), output_field=FloatField()
                )
            ).order_by('-discount_perc', '-id')
        else:
            qs = qs.order_by('-id')
        paginator = Paginator(qs, 12)
        page = request.GET.get('page')
        productList = paginator.get_page(page)
        context['productList'] = productList
        context['sort'] = sort
    return render(request,'search.html', context)


def search_suggest(request):
    """Return JSON suggestions for live search."""
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        qs = Product.objects.filter(
            Q(name__icontains=q) | Q(product_type__icontains=q) | Q(product_gender__icontains=q) | Q(details__icontains=q)
        ).order_by('id')[:8]
        for p in qs:
            results.append({
                'id': p.id,
                'name': p.name,
                'price': float(getattr(p, 'price', 0) or 0),
                'image': p.image1.url if getattr(p, 'image1', None) else '',
                'url': f"/product/{p.id}/",
            })
    return JsonResponse({'results': results})

def home(request):
    slider_items = Slider.objects.filter(is_active=True)
    productList = Product.objects.all()
    featuredProductList = FeaturedProduct.objects.all()
    logo = Logo.objects.all()
    # Random category thumbnails
    male_sample = Product.objects.filter(product_gender="Male", image1__isnull=False).exclude(image1="").order_by('?').first()
    female_sample = Product.objects.filter(product_gender="Female", image1__isnull=False).exclude(image1="").order_by('?').first()
    unisex_sample = Product.objects.filter(product_gender="Unisex", image1__isnull=False).exclude(image1="").order_by('?').first()
    # Roll-ons if product_type is used to denote it; fallback to gender sample
    male_roll_sample = Product.objects.filter(product_gender="Male", product_type__icontains="roll", image1__isnull=False).exclude(image1="").order_by('?').first() or male_sample
    female_roll_sample = Product.objects.filter(product_gender="Female", product_type__icontains="roll", image1__isnull=False).exclude(image1="").order_by('?').first() or female_sample
    unisex_roll_sample = Product.objects.filter(product_gender="Unisex", product_type__icontains="roll", image1__isnull=False).exclude(image1="").order_by('?').first() or unisex_sample
    context = {
        'slider_items': slider_items,
        'productList': productList,
        'featuredProductList': featuredProductList,
        'logolist': logo,
        'male_sample': male_sample,
        'female_sample': female_sample,
        'unisex_sample': unisex_sample,
        'male_roll_sample': male_roll_sample,
        'female_roll_sample': female_roll_sample,
        'unisex_roll_sample': unisex_roll_sample,
    }
    return render(request,'index.html',context)

def about(request):
    # Load dynamic About Page and Delivery Features configured in admin
    from .models import AboutPage, DeliveryFeature

    about_obj = AboutPage.objects.first()

    # Fetch delivery features that are active and intended for the About page (or all pages)
    qs = DeliveryFeature.objects.filter(is_active=True).order_by('sort_order', 'id')
    features = []
    for f in qs:
        pages = (f.pages or '').lower().replace(' ', '')
        page_list = [p for p in pages.split(',') if p] if pages else []
        if not page_list or 'all' in page_list or 'about' in page_list:
            features.append(f)

    context = {
        'about': about_obj,
        'features': features,
    }
    return render(request, 'about.html', context)

def male_Perfume(request):
    sort = request.GET.get('sort', 'new')
    qs = Product.objects.filter(product_gender="Male")
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'name_az':
        qs = qs.order_by('name')
    elif sort == 'name_za':
        qs = qs.order_by('-name')
    elif sort == 'popular':
        qs = qs.annotate(total_sold=Coalesce(Sum('orderitem__quantity'), 0)).order_by('-total_sold', '-id')
    elif sort == 'sale':
        qs = qs.filter(is_sale=True).annotate(
            discount_perc=Case(
                When(price__gt=0, then=ExpressionWrapper((F('price') - F('sale_price')) * Value(100.0) / F('price'), output_field=FloatField())),
                default=Value(0.0), output_field=FloatField()
            )
        ).order_by('-discount_perc', '-id')
    else:
        qs = qs.order_by('-id')
    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    productList = paginator.get_page(page)
    return render(request, 'male_Perfume.html', {'productList': productList, 'sort': sort})

def female_Perfume(request):
    sort = request.GET.get('sort', 'new')
    qs = Product.objects.filter(product_gender="Female")
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'name_az':
        qs = qs.order_by('name')
    elif sort == 'name_za':
        qs = qs.order_by('-name')
    elif sort == 'popular':
        qs = qs.annotate(total_sold=Coalesce(Sum('orderitem__quantity'), 0)).order_by('-total_sold', '-id')
    elif sort == 'sale':
        qs = qs.filter(is_sale=True).annotate(
            discount_perc=Case(
                When(price__gt=0, then=ExpressionWrapper((F('price') - F('sale_price')) * Value(100.0) / F('price'), output_field=FloatField())),
                default=Value(0.0), output_field=FloatField()
            )
        ).order_by('-discount_perc', '-id')
    else:
        qs = qs.order_by('-id')
    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    productList = paginator.get_page(page)
    return render(request, 'female_Perfume.html', {'productList': productList, 'sort': sort})

def unisex_Perfume(request):
    sort = request.GET.get('sort', 'new')
    qs = Product.objects.filter(product_gender="Unisex")
    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'name_az':
        qs = qs.order_by('name')
    elif sort == 'name_za':
        qs = qs.order_by('-name')
    elif sort == 'popular':
        qs = qs.annotate(total_sold=Coalesce(Sum('orderitem__quantity'), 0)).order_by('-total_sold', '-id')
    elif sort == 'sale':
        qs = qs.filter(is_sale=True).annotate(
            discount_perc=Case(
                When(price__gt=0, then=ExpressionWrapper((F('price') - F('sale_price')) * Value(100.0) / F('price'), output_field=FloatField())),
                default=Value(0.0), output_field=FloatField()
            )
        ).order_by('-discount_perc', '-id')
    else:
        qs = qs.order_by('-id')
    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    productList = paginator.get_page(page)
    return render(request, 'unisex_Perfume.html', {'productList': productList, 'sort': sort})

def contact(request):
    # Render dynamic Contact Page content if configured
    try:
        from .models import ContactPage, ContactSubmission
        contact_obj = ContactPage.objects.first()
    except Exception:
        contact_obj = None

    submitted = False
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        subject = (request.POST.get('subject') or '').strip() or 'Website contact'
        message = (request.POST.get('message') or '').strip()
        if name and email and message:
            # Persist submission for admin review
            try:
                ContactSubmission.objects.create(
                    name=name, email=email, phone=phone, subject=subject, message=message
                )
            except Exception:
                pass
            # Try to email the message; fail silently to avoid user disruption in dev
            try:
                from django.core.mail import send_mail
                from django.conf import settings
                recipient = None
                if contact_obj and getattr(contact_obj, 'email', None):
                    recipient = [contact_obj.email]
                else:
                    # Fallback to any configured admin/host user if present
                    host_user = getattr(settings, 'EMAIL_HOST_USER', None)
                    recipient = [host_user] if host_user else None
                if recipient:
                    body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
                    send_mail(subject, body, getattr(settings, 'DEFAULT_FROM_EMAIL', email), recipient, fail_silently=True)
            except Exception:
                pass
            submitted = True
    return render(request, 'contact.html', { 'contact': contact_obj, 'submitted': submitted })

def shop(request):
    sort = request.GET.get('sort', 'new')
    qs = Product.objects.all()

    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    elif sort == 'name_az':
        qs = qs.order_by('name')
    elif sort == 'name_za':
        qs = qs.order_by('-name')
    elif sort == 'popular':
        qs = qs.annotate(total_sold=Coalesce(Sum('orderitem__quantity'), 0)).order_by('-total_sold', '-id')
    elif sort == 'sale':
        qs = qs.filter(is_sale=True).annotate(
            discount_perc=Case(
                When(price__gt=0, then=ExpressionWrapper((F('price') - F('sale_price')) * Value(100.0) / F('price'), output_field=FloatField())),
                default=Value(0.0), output_field=FloatField()
            )
        ).order_by('-discount_perc', '-id')
    else:  # newest
        qs = qs.order_by('-id')

    paginator = Paginator(qs, 6)
    page = request.GET.get('page')
    productList = paginator.get_page(page)
    return render(request,'shop.html',{'productList':productList, 'sort': sort})

def viewProduct(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'elements.html', {'product': product})

def viewFeaturedProduct(request, pk):
    featured_product = get_object_or_404(FeaturedProduct, id=pk)
    product = featured_product.product
    return render(request, 'elements.html', {'product': product})

# ---------------------------
# Other Category Views
# ---------------------------
def cleanserAndFacewash(request):
    productList = Product.objects.all()
    return render(request,'cleanser&Facewash.html',{'productList':productList})

def toner(request):
    productList = Product.objects.all()
    return render(request,'toner.html',{'productList':productList})

def makeup(request):
    productList = Product.objects.all()
    return render(request,'makeup.html',{'productList':productList})

def scerum(request):
    productList = Product.objects.all()
    return render(request,'scerum.html',{'productList':productList})

def moisturizer(request):
    productList = Product.objects.all()
    return render(request,'moisturizer.html',{'productList':productList})

def sunscreen(request):
    productList = Product.objects.all()
    return render(request,'sunscreen.html',{'productList':productList})

# (Roll On category views removed per request)

# ---------------------------
# User Profile View
# ---------------------------
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'orders': orders,
    }
    return render(request, 'profile.html', context)

# ---------------------------
# Cart Views
# ---------------------------
@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total_price = cart.total_price() if items else 0
    return render(request, 'cart.html', {'items': items, 'total_price': total_price})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Read volume/size selection and quantity count (default 1)
    volume_option = '50 ml'
    qty = 1
    if request.method == 'POST':
        volume_option = request.POST.get('volume_option', '50 ml') or '50 ml'
        try:
            qty = int(request.POST.get('quantity', '1'))
        except (TypeError, ValueError):
            qty = 1
        if qty < 1:
            qty = 1

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, volume_option=volume_option
    )
    if created:
        cart_item.quantity = qty
    else:
        cart_item.quantity += qty
    cart_item.save()

    return redirect(request.META.get('HTTP_REFERER', 'shop'))

def buy_now(request, product_id):
    """
    Buy Now functionality: 
    - If user is not logged in, redirect to signin with next parameter
    - If user is logged in, add product to cart and redirect to checkout
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Store the buy_now URL in next parameter to redirect back after login
        from django.urls import reverse
        buy_now_url = reverse('buy_now', args=[product_id])
        signin_url = reverse('signin')
        # Add volume_option to session if POST
        if request.method == 'POST':
            request.session['buy_now_volume'] = request.POST.get('volume_option', '50 ml')
            request.session['buy_now_quantity'] = request.POST.get('quantity', '1')
        return redirect(f"{signin_url}?next={buy_now_url}")
    
    # User is authenticated, add to cart and redirect to checkout
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Get volume option and quantity
    volume_option = '50 ml'
    qty = 1
    
    if request.method == 'POST':
        volume_option = request.POST.get('volume_option', '50 ml') or '50 ml'
        try:
            qty = int(request.POST.get('quantity', '1'))
        except (TypeError, ValueError):
            qty = 1
        if qty < 1:
            qty = 1
    else:
        # Check if we have session data from pre-login
        if 'buy_now_volume' in request.session:
            volume_option = request.session.pop('buy_now_volume', '50 ml')
        if 'buy_now_quantity' in request.session:
            try:
                qty = int(request.session.pop('buy_now_quantity', '1'))
            except (TypeError, ValueError):
                qty = 1
    
    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, volume_option=volume_option
    )
    if created:
        cart_item.quantity = qty
    else:
        cart_item.quantity += qty
    cart_item.save()
    
    # Redirect directly to checkout
    return redirect('checkout')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def ajax_add_to_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({
        'new_quantity': cart_item.quantity,
        'item_total': float(cart_item.total_price())
    })

@login_required
def ajax_remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        new_total = float(cart_item.total_price())
    else:
        new_total = 0
        cart_item.delete()
    return JsonResponse({
        'new_quantity': cart_item.quantity if new_total>0 else 0,
        'item_total': new_total
    })

# ---------------------------
# Checkout Views
# ---------------------------
@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                country=form.cleaned_data['country'],
                order_notes=form.cleaned_data['order_notes'],
                order_status="pending"
            )

            delivery_charge = Decimal("50.00") if form.cleaned_data['country'] == "inside_dhaka" else Decimal("80.00")
            subtotal = cart.total_price()
            order.delivery_charge = delivery_charge
            order.total_price = subtotal + delivery_charge
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    volume_option=getattr(item, 'volume_option', '50 ml')
                )

            cart.items.all().delete()
            return redirect("thank_you")
    else:
        form = CheckoutForm()

    items = cart.items.all()
    return render(request, "checkout.html", {
        "form": form,
        "items": items,
        "total_price": cart.total_price(),
    })

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart.items.all().delete()
            return redirect('thank_you')
    return redirect('checkout')

@login_required
def thank_you(request):
    return render(request, 'thankyou.html')


# ---------------------------
# Export: Order History PDF
# ---------------------------
@login_required
def profile_orders_pdf(request):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.units import mm
    except Exception:  # pragma: no cover
        return HttpResponse("ReportLab is required. Please install 'reportlab' and try again.", status=500)

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_history.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm)
    elements = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#111111'), spaceAfter=8)
    subtitle_style = ParagraphStyle('Sub', parent=styles['Normal'], fontSize=10, textColor=colors.grey)
    section_title = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=12, spaceBefore=8, spaceAfter=6, textColor=colors.HexColor('#111111'))
    cell_style = styles['Normal']

    # Header row with logo and title
    logo_path_candidates = [
        os.path.join(getattr(settings, 'STATIC_ROOT', ''), 'images', 'logonew.png'),
        os.path.join(getattr(settings, 'STATICFILES_DIRS', [os.path.join(settings.BASE_DIR, 'static')])[0], 'images', 'logonew.png') if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS else os.path.join(settings.BASE_DIR, 'static', 'images', 'logonew.png'),
    ]
    logo_img = None
    for lp in logo_path_candidates:
        if lp and os.path.exists(lp):
            try:
                logo_img = Image(lp, width=40*mm, height=14*mm, kind='proportional')
                break
            except Exception:
                pass

    header_cells = [[logo_img if logo_img else Paragraph('<b>Zenko</b>', styles['Heading2']), Paragraph('Order History', title_style)]]
    header_tbl = Table(header_cells, colWidths=[60*mm, None])
    header_tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(header_tbl)
    from datetime import datetime
    elements.append(Paragraph(f"User: {request.user.username} &nbsp;&nbsp; • &nbsp;&nbsp; Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", subtitle_style))
    elements.append(Spacer(1, 8))

    if not orders:
        elements.append(Paragraph('No orders found.', styles['Normal']))
        doc.build(elements)
        return response

    # For each order, build a table
    for order in orders:
        elements.append(Paragraph(f"Order #${order.id}", section_title))

        data = [[
            Paragraph('<b>Product</b>', styles['Normal']),
            Paragraph('<b>Qty</b>', styles['Normal']),
            Paragraph('<b>Price</b>', styles['Normal']),
            Paragraph('<b>Total</b>', styles['Normal']),
        ]]

        for item in order.items.all():
            name = getattr(item.product, 'name', 'Item')
            line_total = item.quantity * item.price
            data.append([
                Paragraph(name, cell_style),
                str(item.quantity),
                f"{item.price} ৳",
                f"{line_total} ৳",
            ])

        # Totals rows
        data.append(['', '', 'Delivery:', f"{getattr(order, 'delivery_charge', 0)} ৳"])
        data.append(['', '', 'Order Total:', f"{order.total_price} ৳"])

        tbl = Table(data, colWidths=[90*mm, 20*mm, 30*mm, 30*mm])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#111111')),
            ('ALIGN', (1,1), (-1,-3), 'RIGHT'),
            ('ALIGN', (0,0), (0,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('FONTNAME', (0,-2), (-1,-2), 'Helvetica'),
            ('GRID', (0,0), (-1,-3), 0.25, colors.HexColor('#E5E7EB')),
            ('LINEABOVE', (-2,-2), (-1,-2), 0.5, colors.HexColor('#E5E7EB')),
            ('LINEABOVE', (-2,-1), (-1,-1), 0.75, colors.HexColor('#9CA3AF')),
            ('BACKGROUND', (-2,-1), (-1,-1), colors.HexColor('#F9FAFB')),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(tbl)

        # Status row
        status = getattr(order, 'order_status', 'pending')
        elements.append(Spacer(1, 4))
        elements.append(Paragraph(f"<font color='#6B7280'>Status:</font> <b>{status.title()}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    return response
