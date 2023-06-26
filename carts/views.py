import re
import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import Resolver404, reverse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldDoesNotExist
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
def cart_view(request) -> HttpResponse:
    """returns: HttpResponse that will query products"""
    items = Cart.objects.filter(user = request.user)
    return render(request, "cart_list.html", {"items": items})


@require_http_methods(['GET'])
def cart_list(request) -> JsonResponse:
    """returns: JsonResponse that contains products"""
    filtered = Cart.objects \
        .filter(user=request.user)

    items = filtered.values(
                "checked",
                "user_id",
                "quantity", 
                "product__handle",
                "product__name",
                "product__price",
                "product__stock")

    image_urls = [cart.product.get_image_url() for cart in filtered]
    book_urls = [cart.product.get_absolute_url() for cart in filtered]

    for i, item in enumerate(items):
        item['image_url'] = image_urls[i]
        item['book_url'] = book_urls[i]

    return JsonResponse({"items": list(items), "statusCode": 200}, safe=False)


@login_required(login_url="/users/signin")
@require_http_methods(['GET'])
def checkout_view(request) -> HttpResponse:
    user = Cart.objects.filter(user=request.user).values("user_id")
    return render(request, "checkout.html", {"items": user})


@require_http_methods(['GET'])
def checkout_list(request) -> JsonResponse:
    """returns: JsonResponse that contains products"""
    filtered = Cart.objects.filter(user=request.user, checked=True)

    if not filtered:
        return JsonResponse({"statusCode": 400})

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
@require_http_methods(['PATCH'])
def cart_update(request):
    """
    expected PATCH request: [
        {op: replace, path: carts/asdf-1, value: {quantity: 3, checked: False}},
        {op: replace, path: carts/asdf-2, value: {quantity: 1: checked: True}},
        ...
    ]
    """
    def get_handle_from_path(url: str):
        pattern = r"carts/(.+)$"
        found = re.search(pattern, url)
        if found:
            return found.group(1)
        raise Resolver404()

    products = Cart.objects.filter(user=request.user)
    json_request = json.loads(request.body)

    # pre check for validation
    if not all([x['op'] == 'replace' for x in json_request]):
        return JsonResponse(
            {"message": "현재는 오직 `replace` op만 사용합니다.",
            "redirect_url": "",
            "statusCode": 400})
    if not all([products\
            .filter(product_id=get_handle_from_path(x['path']))\
            .exists()
            for x in json_request]):
        raise FieldDoesNotExist()

    # let's DO update!
    for each_patch in json_request:
        handle = get_handle_from_path(each_patch['path'])
        newervalue = each_patch['value']
        product = products.get(product_id=handle)

        for key, value in newervalue.items():
            match (key):
                case ('quantity'):
                    product.quantity = value
                case ('checked'):
                    product.checked = value
                case _ :
                    # I'm only care about above.
                    pass
            # end match
        product.save()

    return JsonResponse(
        {"message": "Succesfully update items",
        "statusCode": 200, 
        "redirect_url": reverse("carts:checkout_view")})




@login_required(login_url="/users/signin")
def cart_delete(request):
    if request.method == "DELETE":
        Cart.objects.get(user = request.user, product = get_object_or_404(Product, handle = json.loads(request.body).get("product"))).delete()

        return JsonResponse({"message": "상품을 장바구니에서 삭제했습니다.", "redirect_url": ""})
    else:
        return JsonResponse({"message": "잘못된 접근입니다.", "redirect_url": ""})