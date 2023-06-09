from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import requests
from products.models import Product
from carts.models import Cart
from .models import Purchase, PurchaseItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.urls import reverse
import stripe, json
from core.env import config
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY
KAKAOPAY_SECRET_KEY = config("KAKAOPAY_SECRET_KEY", default=None)
kakaopay_admin_key = KAKAOPAY_SECRET_KEY

@login_required
def stripe_start(request):
    
    BASE_ENDPOINT = f'http://{request.get_host()}'
    data = json.loads(request.body)
    items=data.get('items')

    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    purchase_items=[]
    purchase = Purchase.objects.create(user=request.user)
    product_name = ''
    total_price = 0
    for item in items:
        product = Product.objects.get(handle=item['product__handle'])
        quantity = item['quantity']
        product_name = product.name if not product_name else product_name
        price = product.price * quantity
        purchase_item = PurchaseItem.objects.create(
            purchase=purchase, 
            product=product, 
            quantity=quantity
            )
        total_price += price
        purchase_items.append(purchase_item)
    
    order_name = f'{product_name} 외 {len(items) - 1}' if len(items) > 1 else product_name
    purchase.order_name = order_name

    request.session['purchase_id'] = purchase.id
    
    success_path = reverse("purchases:stripe_success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    
    stopped_path = reverse("purchases:stripe_stopped")
    if not stopped_path.startswith("/"):
        stopped_path = f"/{stopped_path}"

    success_url = f"{BASE_ENDPOINT}{success_path}"
    stopped_url = f"{BASE_ENDPOINT}{stopped_path}"

    line_items = []
    for item in purchase_items:
        line_item = {
            "price": item.stripe_price_id,
            "quantity": item.quantity,
        }
        line_items.append(line_item)

    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        success_url=success_url,
        cancel_url=stopped_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.stripe_price = total_price

    purchase.save()
    return JsonResponse({'checkout_url': checkout_session.url})


@login_required
def stripe_success(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.provider = "stripe"
        purchase.save()

        purchase_items = PurchaseItem.objects.filter(purchase=purchase)
        products = []
        for item in purchase_items:
            item.product.stock -= item.quantity
            products.append(item.product)

        Product.objects.bulk_update(products, ['stock'])
        carts = Cart.objects.filter(product__in=products, user=purchase.user)
        carts.delete()

        del request.session['purchase_id']
        return redirect('/purchases/orders/')
    return JsonResponse({'error': 'Purchase not found'})


@login_required
def stripe_stopped(request):
    BASE_ENDPOINT = f'http://{request.get_host()}'
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        del request.session['purchase_id']
        purchase.delete()
        cart_view_url = f'{BASE_ENDPOINT}{reverse("carts:view")}'
        return redirect(cart_view_url)
    return HttpResponse("Purchase not found")


@login_required
def kakaopay_start(request):
    BASE_ENDPOINT = f'http://{request.get_host()}'
    data = json.loads(request.body)
    
    items = data.get('items')
    
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    products = []
    total_price, price = 0, 0
    items_count = len(items)
    purchase = Purchase.objects.create(user=request.user)
    product_name = ''
    for item in items:
        product_handle = item['product__handle']
        product = Product.objects.get(handle=product_handle)
        product_quantity = item['quantity']
        product_name = product.name if not product_name else product_name

        PurchaseItem.objects.create(purchase=purchase, product=product, quantity=product_quantity)
        price = product.price * product_quantity
        total_price += price
        products.append(product)
    
    if items_count > 1:
        order_name = f'{product_name} 외 {items_count - 1}'
    else:
        order_name = product_name
    
    purchase.order_name = order_name
    purchase.kakaopay_price = total_price

    request.session['purchase_id'] = purchase.id

    success_path = reverse("purchases:kakaopay_success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"

    stopped_path = reverse("purchases:kakaopay_stopped")
    if not stopped_path.startswith("/"):
        stopped_path = f"/{stopped_path}"

    success_url = f"{BASE_ENDPOINT}{success_path}"
    stopped_url = f"{BASE_ENDPOINT}{stopped_path}"

    url = f'https://kapi.kakao.com/v1/payment/ready'
    header = {
        'Authorization': f'KakaoAK {kakaopay_admin_key}'
    }

    data = {
        'cid': 'TC0ONETIME', # 테스트용 기본 가맹점 키 값
        'partner_order_id': purchase.id,
        'partner_user_id': 'partner_user_id', # 테스트용 기본 데이터
        'item_name': order_name,
        'quantity': 1,
        'total_amount': int(total_price),
        'tax_free_amount': 0,
        'approval_url': success_url,
        'fail_url': stopped_url,
        'cancel_url': stopped_url
    }
    
    res = requests.post(url, data=data, headers=header)
    result = res.json()
    
    purchase.kakaopay_checkout_tid = result['tid']
    purchase.provider = 'kakaopay'
    purchase.save()
    return JsonResponse({'redirect': result['next_redirect_pc_url']})


@login_required
def kakaopay_success(request):
    purchase_id = request.session.get('purchase_id')
    if not(purchase_id):
        return HttpResponseBadRequest()
    
    purchase = Purchase.objects.get(id=purchase_id)
    if purchase is None:
        return HttpResponseBadRequest()
    
    tid = purchase.kakaopay_checkout_tid
    if not(tid):
        return HttpResponseBadRequest()
    
    url = f'https://kapi.kakao.com/v1/payment/approve'
    header = {
        'Authorization': f'KakaoAK {kakaopay_admin_key}'
    }
    data = {
        'cid': 'TC0ONETIME', # 테스트용 기본 가맹점 키 값
        'tid': tid,
        'partner_order_id': purchase_id,
        'partner_user_id': 'partner_user_id', # 테스트용 기본 데이터
        'pg_token': request.GET['pg_token']
    }

    res = requests.post(url, data=data, headers=header)
    result = res.json()
    
    if result.get('msg'):
        return JsonResponse({'error': 'Purchase not found'})
    
    purchase_items = PurchaseItem.objects.filter(purchase=purchase)
    products = []
    for item in purchase_items:
        item.product.stock -= item.quantity
        products.append(item.product)

    Product.objects.bulk_update(products, ['stock'])
    carts = Cart.objects.filter(product__in=products, user=purchase.user)
    carts.delete()

    purchase.completed = True
    purchase.save()
    del request.session['purchase_id']
    return redirect('/purchases/orders/')
    

@login_required
def kakaopay_stopped(request):
    BASE_ENDPOINT = f'http://{request.get_host()}'
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.delete()
        del request.session['purchase_id']
        
        cart_view_url = f'{BASE_ENDPOINT}{reverse("carts:view")}'
        return redirect(cart_view_url)
            
    return HttpResponse("Purchase not found")


def stripe_payment_cancel(purchase):
    if purchase.stripe_checkout_session_id:
        try:
            session = stripe.checkout.Session.retrieve(purchase.stripe_checkout_session_id)
            if session.payment_status == 'paid':
                payment_intent_id = session.payment_intent
                amount = session.amount_total

                refund = stripe.Refund.create(
                    payment_intent=payment_intent_id,
                    amount=amount,
                )
                
                if refund.status == 'succeeded':
                    purchase_items = PurchaseItem.objects.filter(purchase=purchase)
                    products = []
                    for item in purchase_items:
                        item.product.stock += item.quantity
                        products.append(item.product)

                    Product.objects.bulk_update(products, ['stock'])
                        
                    purchase.completed = False
                    purchase.save()
                    return True
                else:
                    return False
            else:
                return False
        except stripe.error.StripeError as e:
            print(str(e))
            return False
   
    return False


def kakaopay_payment_cancel(purchase):
    tid = purchase.kakaopay_checkout_tid
    total_price = purchase.kakaopay_price
    
    url = f'https://kapi.kakao.com/v1/payment/cancel'
    header = {
        'Authorization': f'KakaoAK {kakaopay_admin_key}'
    }

    data = {
        'cid': 'TC0ONETIME', # 테스트용 기본 가맹점 키 값
        'tid': tid,
        'cancel_amount': total_price,
        'cancel_tax_free_amount': 0
    }

    res = requests.post(url, data=data, headers=header)
    result = res.json()

    if result.get('msg'):
        return False

    purchase_items = PurchaseItem.objects.filter(purchase=purchase)
    products = []
    for item in purchase_items:
        item.product.stock += item.quantity
        products.append(item.product)

    Product.objects.bulk_update(products, ['stock'])

    purchase.completed = False
    purchase.save()
    return True


@login_required
def purchase_order_view(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, "orders.html", {"purchases": purchases})


@login_required
def payment_cancel(request, purchase_id):
    if request.method == "POST":
        purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user, completed=True)
        is_success = False

        match(purchase.provider):
            case "stripe":
                is_success = stripe_payment_cancel(purchase)
            case "kakaopay":
                is_success = kakaopay_payment_cancel(purchase)
        
        if is_success:
            return redirect('purchases:orders')
        
        return HttpResponse("Failed to cancel")
    
    return HttpResponseBadRequest()

