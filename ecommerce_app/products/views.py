from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.detail import DetailView
    #from .models import

def testController(request):
    context = {
        "name": "Ayush Shr",
    }
    return render(request, 'products/products_list.html', context)

