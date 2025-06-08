from django.shortcuts import render, redirect
from .models import Product,CartItem
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
# Create your views here.
@login_required(login_url='/login/')
def product_list(request):
  products=Product.objects.all()
  return render(request, 'cart/index.html', {'products':products})      
   
def view_cart(request):
  cart_items = CartItem.objects.filter(user=request.user)
  total_price = sum(item.product.price * item.quantity for item in cart_items)
  return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required(login_url='/login/')
def add_to_cart(request, product_id):
  product =Product.objects.get(id=product_id)
  cart_item, created = CartItem.objects.get_or_create(product=product,
                                                      user=request.user)
  cart_item.quantity += 1  
  cart_item.save()
  return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
  cart_item = CartItem.objects.get(id=item_id)
  if cart_item.quantity==1:
    cart_item.delete()
  else:
    cart_item.quantity-=1
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

        #This now runs only if username is not taken
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
