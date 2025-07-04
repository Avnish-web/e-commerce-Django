from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from cart import views as cart_views
from django.views.generic import TemplateView
#from paypal.standard.ipn import urls as paypal_urls
from cart import api_views  # Ensure this exists
#from cart.api_views import example_api



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cart.urls')),
    path('cart/', include('cart.urls')),
    path('login/', cart_views.login_page, name='login_page'),
    path('register/', cart_views.register_page, name='register'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('logout/', cart_views.signout, name='logout'),
    #path('paypal/', include(paypal_urls)),
    path('payment_process/', api_views.payment_process, name='payment_process'),
    path('payment_done/', TemplateView.as_view(template_name="pets/payment_done.html"), name='payment_done'),
    path('payment_canceled/', TemplateView.as_view(template_name="pets/payment_canceled.html"), name='payment_canceled'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
