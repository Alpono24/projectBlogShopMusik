from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Product, Category, CurrencyRateUSD, CurrencyRateEUR, CartItem, Order, Seller, OrderDetail
import logging
from pathlib import Path
from django.shortcuts import render, redirect
from .tasks import send_customer_email, send_admin_new_order_email, clean_cart


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / 'shop' / 'log_file'

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)

CART_LOG_PATH = LOG_DIR / 'log_cart.log'

cart_logger = logging.getLogger('cart')
cart_logger.setLevel(logging.DEBUG)

cart_handler = logging.FileHandler(CART_LOG_PATH)
cart_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
cart_logger.addHandler(cart_handler)


def products_view(request):
    title = 'МАГАЗИН'
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    query = request.GET.get('q')
    products = Product.objects.all()

    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query)
        ).distinct()

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'title': title,
        'page_obj': page_obj,
        'rate_usd': rate_usd,
        'rate_eur': rate_eur,
    })



@login_required(login_url='/registration/login/')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

    return render(request, 'product_detail.html', {
        'product': product,
        'rate_usd': rate_usd,
        'rate_eur': rate_eur,
    })



@login_required(login_url='/registration/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        requested_quantity = int(request.POST.get('quantity', 1))
        existing_cart_items = CartItem.objects.filter(user=request.user, product=product)

        current_total_quantity = sum(item.quantity for item in existing_cart_items) + requested_quantity

        if current_total_quantity > product.quantity:
            return redirect('products:cart_view')

        for cart_item in existing_cart_items:
            cart_item.quantity += requested_quantity
            cart_item.save()
            break
        else:
            CartItem.objects.create(user=request.user, product=product, quantity=requested_quantity)

        return redirect('products:cart_view')
    else:
        context = {'product': product}
        return render(request, 'add_to_cart_form.html', context)



@login_required(login_url='/registration/login/')
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        cart_item.delete()
        cart_logger.info(f"Товар -> '{product.name}' успешно удалён из корзины.")
    except CartItem.DoesNotExist:
        cart_logger.info(f"Ошибка удаления товара {product.name} из корзины")
    return redirect('products:cart_view')


@login_required(login_url='/registration/login/')
def delete_selected_products(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_item', [])
        if not selected_items:
            return redirect('products:cart_view')
        selected_items = map(int, selected_items)
        items = CartItem.objects.filter(pk__in=selected_items, user=request.user)
        names = ', '.join([item.product.name for item in items])
        items.delete()

        cart_logger.info(f"Выбранные товары ({names}) были успешно удалены из вашей корзины.")
    return redirect('products:cart_view')



@login_required(login_url='/registration/login/')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()
    return render(request, 'products_cart.html',
                  {'products': cart_items, 'total': total,'rate_usd': rate_usd, 'rate_eur': rate_eur,})



@login_required(login_url='/registration/login/')
def pre_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()
    return render(request, 'pre_order.html',
                  {'products': cart_items, 'total': total,'rate_usd': rate_usd, 'rate_eur': rate_eur,})



@login_required(login_url='/registration/login/')
def mark_items_as_selected(request):
    if request.method == 'POST':
        all_user_cart_items = list(CartItem.objects.filter(user=request.user))

        selected_items_ids = request.POST.getlist('selected_item', [])

        for item in all_user_cart_items:
            if str(item.pk) in selected_items_ids:
                item.selected = True
            else:
                item.selected = False
            item.save()

        return redirect('products:pre_order')
    return None



@login_required(login_url='/registration/login/')
def pre_order_confirmation(request):
    if request.method == 'POST':

        cart_items = CartItem.objects.filter(user=request.user, selected=True)
        total_amount = sum([item.total_price() for item in cart_items])

        rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
        rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

        return render(request, 'pre_order_confirmation.html', {
            'products': cart_items,
            'total_amount': total_amount,
            'rate_usd': rate_usd,
            'rate_eur': rate_eur,
            'user': request.user,
        })

    else:
        return redirect('products:products')



@login_required(login_url='/registration/login/')
def create_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user, selected=True)

        unavailable_products = []
        for item in cart_items:
            if item.product.quantity == 0 or not item.product.in_stock:
                unavailable_products.append(item.product.name)

        if unavailable_products:
            cart_logger.info(request, f"Следующие товары временно отсутствуют: {', '.join(unavailable_products)}")
            return redirect('products:pre_order')

        total_amount = sum([item.total_price() for item in cart_items])
        new_order = Order.objects.create(user=request.user, total_amount=total_amount)

        details = []
        for item in cart_items:
            detail = OrderDetail(
                order=new_order,
                product=item.product,
                quantity=item.quantity,
            )
            details.append(detail)
        OrderDetail.objects.bulk_create(details)

        order_items_list = OrderDetail.objects.filter(order=new_order)

        rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
        rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

        return render(request, 'order.html', {
            'order': new_order,
            'products': order_items_list,
            'rate_usd': rate_usd,
            'rate_eur': rate_eur,
            'order_id': new_order.pk,
            'total_amount': total_amount,
        })
    else:
        return redirect('products:cart_view')


@login_required(login_url='/registration/login/')
def send_email_sell(request, order_id):
    cart_logger.info("Завершающий этап оформления заказа: send_email_sell")
    try:
        # raise ValueError (f"переход на Exception для проверки products:error_confirm_order")
        with transaction.atomic():
            cart_logger.info("Начало работы  - send_email_sell")

            order = Order.objects.select_for_update().get(pk=order_id)

            if order.is_sent:
                messages.warning(request, "Этот заказ уже был обработан.")
                return redirect('products:order_is_sent')

            for order_item in order.details.all():
                product = order_item.product
                available_quantity = product.quantity
                purchased_quantity = order_item.quantity

                if available_quantity >= purchased_quantity:
                    product.quantity -= purchased_quantity
                    product.save()
                else:
                    raise ValueError(f"Товар '{product.name}' отсутствует в нужном количестве.")

            order.is_sent = True
            order.save()

            cart_logger.info("Старт отправки писем через Celery")
            send_customer_email.delay(order.id)
            send_admin_new_order_email.delay(order.id)

            cart_logger.info("Старт задачи на очистку корзины через Celery")
            clean_cart.delay(request.user.id, order_id)

            return redirect('products:checkout_success')

    except Exception as e:
        cart_logger.error(f"Произошла ошибка отправки писем: {e}")
        return redirect('products:error_confirm_order')



@login_required(login_url='/registration/login/')
def error_confirm_order(request):
    order = Order.objects.filter(user=request.user).latest('id')
    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

    return render(request, 'error_confirm_order.html', {
        'order': order,
        'rate_usd': rate_usd,
        'rate_eur': rate_eur,
    })



@login_required(login_url='/registration/login/')
def order_is_sent(request):
    order = Order.objects.filter(user=request.user).latest('id')
    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

    return render(request, 'order_is_sent.html', {
        'order': order,
        'rate_usd': rate_usd,
        'rate_eur': rate_eur,
    })


@login_required(login_url='/registration/login/')
def checkout_success(request):
    order = Order.objects.filter(user=request.user).latest('id')
    rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
    rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

    return render(request, 'checkout_success.html', {
        'order': order,
        'rate_usd': rate_usd,
        'rate_eur': rate_eur,
    })



def handler404(request, exception=None):
    return render(request, 'errors/404.html', {'path': request.path}, status=404)



def handler500(request):
    return render(request, 'errors/500.html', {}, status=500)


