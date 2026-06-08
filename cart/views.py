from django.shortcuts import redirect, render
from django.conf import settings
from products.models import Product, Order, SiteSettings
import requests


def send_telegram_message(order, products):
    products_text = ""

    for product in products:
        products_text += (
            f"📦 {product.name}\n"
            f"🔢 الكمية: {product.qty}\n"
            f"💵 السعر: {product.price} جنيه\n"
            f"💰 الإجمالي: {product.total_price} جنيه\n\n"
        )

    message = f"""
🛒 طلب جديد

👤 الاسم: {order.name}
📞 الهاتف: {order.phone}
📞 هاتف إضافي: {order.phone2 or '-'}
🏙️ المدينة: {order.city}
📍 العنوان: {order.address}
💳 الدفع: {order.payment_method}

━━━━━━━━━━━━━━

{products_text}

━━━━━━━━━━━━━━

💰 إجمالي المنتجات: {order.total_price} جنيه
🆔 رقم الطلب: #{order.id}
"""

    requests.post(
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        data={
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": message
        },
        timeout=10
    )

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)
    qty = int(request.POST.get('quantity', 1))

    cart[product_id] = cart.get(product_id, 0) + qty

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        product.qty = qty
        product.total_price = product.price * qty

        total += product.total_price
        products.append(product)

    return render(request, 'cart/cart.html', {
        'products': products,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})

    settings_obj = SiteSettings.objects.first()
    shipping_cost = settings_obj.shipping_cost if settings_obj else 80

    products = []
    subtotal = 0

    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            continue

        product.qty = qty
        product.total_price = product.price * qty

        subtotal += product.total_price
        products.append(product)

    total = subtotal + shipping_cost

    if request.method == 'POST':
        order = Order.objects.create(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            phone2=request.POST.get('phone2'),
            city=request.POST.get('city'),
            payment_method=request.POST.get('payment_method'),
            total_price=total
        )

        try:
            send_telegram_message(order, products)
        except Exception:
            pass

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('success')

    return render(request, 'cart/checkout.html', {
        'products': products,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total': total
    })


def success(request):
    return render(request, 'cart/success.html')