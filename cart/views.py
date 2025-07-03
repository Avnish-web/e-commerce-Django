from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
import json

from .models import Product, CartItem, Order
#from paypal.standard.forms import PayPalPaymentsForm


def payment_process(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '100',
        'item_name': 'Item_Name_xyz',
        'invoice': 'Test Payment Invoice',
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment_done")}',
        'cancel_return': f'http://{host}{reverse("payment_canceled")}',
    }
    #form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'pets/payment_process.html', {})

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        payment = client.order.create({
            "amount": int(product.price * 100),
            "currency": "INR",
            "payment_capture": "1"
        })

        return render(request, 'orders/buy_now.html', {
            'product': product,
            'payment': payment,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID
        })

    return render(request, 'cart/buy_now.html', {'product': product})

@login_required
def place_order(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        address = request.POST['address']
        product = get_object_or_404(Product, id=product_id)

        Order.objects.create(
            user=request.user,
            product=product,
            address=address,
            amount=product.price,
            payment_status='Paid'
        )

        return render(request, 'cart/order_success.html', {'product': product})

    return redirect('cart:product_list')

@login_required(login_url='/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'cart/index.html', {'products': products})

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart:view_cart')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password')
            return redirect('/login/')

        login(request, user)
        return redirect('cart:product_list')

    return render(request, 'cart/login.html')

@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already registered...!")
            return redirect('/register/')

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "Account Created Successfully...!")
        return redirect('/login/')

    return render(request, 'cart/register.html')

def signout(request):
    logout(request)
    return redirect("/login/")

@csrf_exempt
def update_quantity(request, item_id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            action = data.get("action")
            item = CartItem.objects.get(id=item_id, user=request.user)

            if action == "increase":
                item.quantity += 1
            elif action == "decrease":
                item.quantity -= 1

            if item.quantity <= 0:
                item.delete()
                total = sum(i.product.price * i.quantity for i in CartItem.objects.filter(user=request.user))
                return JsonResponse({"success": True, "removed": True, "updated_total": total})

            item.save()
            total = sum(i.product.price * i.quantity for i in CartItem.objects.filter(user=request.user))

            return JsonResponse({
                "success": True,
                "removed": False,
                "new_quantity": item.quantity,
                "updated_total": total
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})
