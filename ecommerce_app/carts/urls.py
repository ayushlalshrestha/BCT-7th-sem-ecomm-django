from django.conf.urls import  url
#from django.conf.urls.static import static
#from django.contrib import admin
from . import views
from orders.views import CheckoutView, UserAddressCreateView

urlpatterns = [
    url(r'^$', views.CartView.as_view() , name='cart'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', UserAddressCreateView.as_view(), name='user_address_create'),
    #url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),

]