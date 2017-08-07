from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from .models import Product, Variation


def product_search(request):
    if request.method == "POST":
        keyword = request.POST.get("keyword")
    else:
        keyword = request.GET.get("keyword")
    
    variation_list = Variation.objects.all()
    product_list = []
    for variation in variation_list:
        variation_str = (variation.product.title + " " + variation.product.product_id + " "  + variation.product.manufacturer +  " "  + variation.title + " " + variation.product.category.title).lower()
        print(variation_str)
        #if (variation.product.title.find(keyword) != -1 or variation.product.product_id.find(keyword) != -1 or variation.product.manufacturer.find(keyword) != -1 or variation.title.find(keyword) != -1):
        if variation_str.find(keyword.lower()) != -1:
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
        product_category = context.get("object").category.title
        product_sub_category = context.get("object").sub_category
        product_relatable_keyword = context.get("object").relatable_keyword
        print(product_category + " " + product_sub_category )
        #-------------------  Recommendation ---- 
        variation_list = Variation.objects.all()
        similar_items = []
        for variation in variation_list:
            if ((variation.product.category.title == product_category and variation.product.sub_category == product_sub_category) or variation.product.relatable_keyword == product_relatable_keyword):
                if ((not variation.product in similar_items) and (variation.product != context.get("object") )):
                    similar_items.append(variation.product)
        context["similar_items"] = similar_items    
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
        most_popular_brands = ["Apple Computers", "Samsung Group", "Microsoft" ,"Lenovo", "HTC"]
        context["user_status"] = user_status
        context["most_popular_brands"] = most_popular_brands
        return context

    