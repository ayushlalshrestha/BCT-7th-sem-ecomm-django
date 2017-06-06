from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Product


def testcontroller(request):
    context = {
        "name": "Ayush Shr",
    }
    return render(request, 'products/products_list.html', context)

class ProductDetailView(DetailView):
    model = Product
    #template_name = "<appname>/<modelname>_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            user_status = self.request.user.first_name
        else:
            user_status = "NOT LOGGED IN"
        context["user_status"] = user_status
        return context

    