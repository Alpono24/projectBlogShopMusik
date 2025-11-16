from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category

# Create your views here.

def products_view(request):
    title = 'Товары'
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    query = request.GET.get('q')
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        ).distinct()
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'title': title,
        'page_obj': page_obj
    })



@login_required(login_url='/registration/login/')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


@login_required(login_url='/registration/login/')
def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart
    return redirect('products:cart_view')

@login_required(login_url='/registration/login/')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('products:cart_view')


@login_required(login_url='/registration/login/')
def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'products_cart.html', {'products': products, 'total': total})
