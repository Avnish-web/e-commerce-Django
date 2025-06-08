from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
#from cart.views import *
from cart import views as cart_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cart.urls')),
    path('login/', cart_views.login_page, name='login_page'),
    path('register/', cart_views.register_page, name='register'),
    path('logout/', cart_views.signout, name='logout')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
