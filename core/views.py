from django.shortcuts import render
from products.models import Product

def home(request):
    latest_products = Product.objects.order_by('-id')[:4]

    return render(request, 'index.html', {
        'latest_products': latest_products
    })