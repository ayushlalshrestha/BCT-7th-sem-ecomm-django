from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Product, Variation


def product_search(request):
    keyword = request.POST.get("keyword")
    variation_list = Variation.objects.all()
    product_list = []
    for variation in variation_list:
        #if ((variation.product.title.find(keyword) >= 0) or (variation.product.product_id.find(keyword) != -1) or (variation.product.manufacturer.find(keyword) != -1) or (variation.title.find(keyword) != -1)):
        if (variation.product.title.find(keyword) != -1 or variation.product.product_id.find(keyword) != -1 or variation.product.manufacturer.find(keyword) != -1 or variation.title.find(keyword) != -1):
            if not variation.product in product_list:
                product_list.append(variation.product)
    if len(product_list) == 0:
        empty_result = True
    else:
        empty_result = False    
    context = {
        "product_list":  product_list,
        "passed_keyword":  keyword,
        "product_list_length": len(product_list),
        "empty_result": empty_result,
    }
    return render(request, 'products/search_result.html', context)
    

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

    