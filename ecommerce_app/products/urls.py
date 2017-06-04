from django.conf import settings
from django.conf.urls import  url
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.testController , name='testcontroller'),
    #url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail'),

]