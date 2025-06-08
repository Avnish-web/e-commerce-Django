from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # homepage -> product list
    path('login/', views.login_page, name='login_page'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.signout, name='logout'),

    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
