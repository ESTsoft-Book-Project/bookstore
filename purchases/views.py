from django.shortcuts import render, redirect
from products.models import Product
from .models import Purchase
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse
import stripe, json
from core.env import config
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY

@login_required
def purchase_start_view(request):
    
    BASE_ENDPOINT = f'http://{request.get_host()}'
    data = json.loads(request.body)
    handle = data.get('handle')

    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    product = Product.objects.get(handle=handle)
    stripe_price_id = product.stripe_price_id
    
    if stripe_price_id is None:
        return HttpResponseBadRequest()
    
    purchase = Purchase.objects.create(user=request.user, product=product)
    request.session['purchase_id'] = purchase.id
    
    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    
    stopped_path = reverse("purchases:stopped")
    if not stopped_path.startswith("/"):
        stopped_path = f"/{stopped_path}"

    success_url = f"{BASE_ENDPOINT}{success_path}"
    stopped_url = f"{BASE_ENDPOINT}{stopped_path}"

    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity":1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=stopped_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.stripe_price = product.price

    purchase.save()
    return JsonResponse({'checkout_url': checkout_session.url})

from django.http import JsonResponse

@login_required
def purchase_success_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
        del request.session['purchase_id']
        return redirect('/purchases/orders/')
    return JsonResponse({'error': 'Purchase not found'})


@login_required
def purchase_stopped_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        del request.session['purchase_id']
        return redirect(purchase.product.get_absolute_url())
    return HttpResponse("Purchase not found")


@login_required
def purchase_order_view(request):
    purchases = Purchase.objects.filter(user=request.user, completed=True)
    return render(request, "orders.html", {"purchases": purchases})
