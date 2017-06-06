from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views.generic.base import View
# from django.views.generic import View
from .forms import MyRegistrationForm



# Create your views here.
class login(View):
    def get(self, request):
        if self.request.user.is_authenticated:
            login_status = "LOGGED IN as " + str(self.request.user.first_name)
        else:
            login_status = "NOT LOGGED IN"
        context = {
            "login_status": login_status,
        }
        return render(request, "users/login_page.html", context)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return HttpResponseRedirect("/products?login_success=True")
        else:
            print("Not Done !!")
            return HttpResponseRedirect("/users?login_fail=True")


def logout(request):
    if request.user:
        auth.logout(request)
    return HttpResponseRedirect("/users?logout_success=True")


# New User Creation
def new_user_creation(request):
    if request.method == "POST":
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/users?new_creation=True/")
        else:
            raise forms.ValidationError("Some Error during Data Entry !!")
    else:
        form = MyRegistrationForm()
        context = {
            "form" : form,
        }
        return render(request, "users/new_user_register.html", context)
