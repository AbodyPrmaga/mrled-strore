from django.shortcuts import render, get_object_or_404,redirect
from .models import Product, Order, SiteSettings

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'products/products.html', {'products': products})



def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    settings = SiteSettings.objects.first()

    message = None

    if request.method == "POST":

        quantity = int(request.POST.get("quantity", 1))
        shipping = settings.shipping_cost if settings else 80

        price = product.discount_price or product.price

        total = (price * quantity) + shipping

        Order.objects.create(
            product=product,
            quantity=quantity,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            phone2=request.POST.get("phone2"),
            city=request.POST.get("city"),
            address=request.POST.get("address"),
            payment_method=request.POST.get("payment_method"),

            # 🔥 حفظ القيم
            product_price=price,
            shipping_cost=shipping,
            total_price=total,
        )

        message = "تم تسجيل الطلب بنجاح!!"

    return render(request, "products/product_detail.html", {
        "product": product,
        "settings": settings,
        "message": message
    })