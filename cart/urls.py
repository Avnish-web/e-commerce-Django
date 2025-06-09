from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('update-quantity/', views.update_quantity, name='update_quantity'),
    path('', views.product_list, name='product_list'),  
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.signout, name='logout'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('products/', views.product_list, name='product_list'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/', views.view_cart, name='view_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]