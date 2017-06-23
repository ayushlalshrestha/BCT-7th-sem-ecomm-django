from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView

from .forms import UserAddressForm, GuestCheckoutForm
from .models import UserAddress, UserCheckout, Order
from .mixins import CartOrderMixin, LoginRequiredMixin
from carts.models import Cart


class UserAddressCreateView(CartOrderMixin, CreateView):
    form_class = UserAddressForm
    template_name = "orders/useraddress_create.html"
    
    def get_checkout_user(self):
        user_check_id = self.request.session.get("user_checkout_id")
        if user_check_id == None:
            return None
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return user_checkout

    def get_success_url(self):
        return reverse("checkout_final")    

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        if form.instance.user != None:
            print(form.instance)
            print(type(form.instance))
            print(" - - - - - - - - - - - - - - ")
            new_order = self.get_order()
            self.request.session["order_pk"] = new_order.pk
            new_order.user = self.get_checkout_user()
            form.instance.save()
            new_order.shipping_address = form.instance
            new_order.save()
            return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)
        return redirect("checkout")    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CheckoutView(CartOrderMixin, FormMixin, DetailView):
    model = Cart
    template_name = "orders/checkout_view.html"
    form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        if cart == None:
            return None
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_can_continue = False
        user_check_id = self.request.session.get("user_checkout_id")
        if self.request.user.is_authenticated():
            user_can_continue = True
            user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
            user_checkout.user = self.request.user
            user_checkout.save()
            #context["client_token"] = user_checkout.get_client_token()
            self.request.session["user_checkout_id"] = user_checkout.id
        elif not self.request.user.is_authenticated() and user_check_id == None:
            context["login_form"] = AuthenticationForm()
            context["next_url"] = self.request.build_absolute_uri()
        else:
            pass

        if user_check_id != None:
            user_can_continue = True
            if not self.request.user.is_authenticated():  # GUEST USER
                user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
               #context["client_token"] = user_checkout_2.get_client_token()
        context["user_can_continue"] = user_can_continue
        context["form"] = self.get_form()
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            request.session["user_checkout_id"] = user_checkout.id
            print(" ----------------------   Yes a new Checkout user has been created !!")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("checkout")

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if cart == None:
            return redirect("cart")
        #* new_order = self.get_order()
        user_checkout_id = request.session.get("user_checkout_id")
        if user_checkout_id != None:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            print("------------------------------------------- i am here !!")
            return redirect("user_address_create")
        return get_data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class CheckoutFinalView(CartOrderMixin, View):
    def post(self, request, *args, **kwargs):
        order = self.get_order()
        order_total = order.order_total
        nonce = request.POST.get("payment_method_nonce")
        if nonce:
            result = braintree.Transaction.sale({
			    "amount": order_total,
			    "payment_method_nonce": nonce,
			    "billing": {
				    "postal_code": "%s" %(order.shipping_address.zipcode),
				    
				 },
			    "options": {
			        "submit_for_settlement": True
			    }
			})
            if result.is_success:
                #result.transaction.id to order
                order.mark_completed(order_id=result.transaction.id)
                messages.success(request, "Thank you for your order.")
                del request.session["cart_id"]
                del request.session["order_id"]
            else:
				#messages.success(request, "There was a problem with your order.")
                messages.success(request, "%s" %(result.message))
                return redirect("checkout")

        return redirect("order_detail", pk=order.pk)

    def get(self, request, *args, **kwargs):
        user_check_id = self.request.session.get("user_checkout_id")
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        
        order_pk = self.request.session.get("order_pk")
        order = Order.objects.get(pk = order_pk)
        client_token = user_checkout.get_client_token()
        context = {
            "order": order,
            "client_token": client_token,
        }
        context["client_token"] = user_checkout.get_client_token()
        return render(request, "orders/checkout_final.html", context)



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class OrderList(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
 
    def get_queryset(self):
        user_check_id = self.request.user.id
        user_checkout = UserCheckout.objects.get(id=user_check_id)
        return super(OrderList, self).get_queryset().filter(user=user_checkout)