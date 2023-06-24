import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from .forms import CartForm
from .models import Cart
from .models import Product


@login_required(login_url="/users/signin")
def cart_add(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        request_data["user"] = request.user
        request_data["product"] = get_object_or_404(Product, handle = request_data.get("product"))

        try:
            item = Cart.objects.get(user = request_data["user"], product = request_data["product"])
            if item:
                item.quantity += 1
                item.save()
                return JsonResponse({"message": "장바구니 담기에 성공했습니다.", "redirect_url": "/carts"})
        except:
            request_data["quantity"] = 1
        
        form = CartForm(request_data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "장바구니 담기에 성공했습니다.", "redirect_url": "/carts"})
        else:
            return JsonResponse({"message": form.errors.as_json()})


@login_required(login_url="/users/signin")
@require_http_methods(['GET'])
def cart_list(request) -> HttpResponse:
    """returns: HttpResponse that will query products"""
    items = Cart.objects.filter(user = request.user)
    return render(request, "cart_list.html", {"items": items})


@require_http_methods(['GET'])
def product_list(request) -> JsonResponse:
    """returns: JsonResponse that contains products"""
    filtered = Cart.objects \
        .filter(user=request.user)

    items = filtered.values(
                "checked",
                "user_id",
                "quantity", 
                "product__handle",
                "product__name",
                "product__price")

    image_urls = [cart.product.get_image_url() for cart in filtered]
    book_urls = [cart.product.get_absolute_url() for cart in filtered]

    for i, item in enumerate(items):
        item['image_url'] = image_urls[i]
        item['book_url'] = book_urls[i]

    return JsonResponse({"items": list(items), "statusCode": 200}, safe=False)


@login_required(login_url="/users/signin")
@require_http_methods(['GET'])
def order_detail(request) -> HttpResponse:
    user = Cart.objects.filter(user=request.user).values("user_id")
    return render(request, "order_detail.html", {"items": user})


@require_http_methods(['GET'])
def order_product_detail(request) -> JsonResponse:
    """returns: JsonResponse that contains products"""
    filtered = Cart.objects.filter(user=request.user, checked=True)

    items = filtered.values(
                "checked",
                "user_id",
                "quantity", 
                "product__handle",
                "product__name",
                "product__price")

    image_urls = [cart.product.get_image_url() for cart in filtered]
    book_urls = [cart.product.get_absolute_url() for cart in filtered]


    for i, item in enumerate(items):
        item['image_url'] = image_urls[i]
        item['book_url'] = book_urls[i]

    print(items)

    return JsonResponse({"items": list(items), "statusCode": 200}, safe=False)


@login_required(login_url="/users/signin")
def cart_update(request):
    if request.method == 'PATCH':
        item = Cart.objects.get(user = request.user, product = get_object_or_404(Product, handle = json.loads(request.body).get("product")))
        item.quantity = json.loads(request.body)["quantity"]
        item.save()

        return JsonResponse({"redirect_url": "", "status_code": 200})
    else:
        return JsonResponse({"message": "잘못된 접근입니다.", "redirect_url": "", "status_code": 400})


@login_required(login_url="/users/signin")
def cart_delete(request):
    if request.method == "DELETE":
        Cart.objects.get(user = request.user, product = get_object_or_404(Product, handle = json.loads(request.body).get("product"))).delete()

        return JsonResponse({"message": "상품을 장바구니에서 삭제했습니다.", "redirect_url": ""})
    else:
        return JsonResponse({"message": "잘못된 접근입니다.", "redirect_url": ""})