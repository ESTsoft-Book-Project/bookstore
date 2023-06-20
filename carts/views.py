from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CartForm
from .models import Cart
from .models import Product
import json


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
def cart_list(request):
    items = Cart.objects.filter(user = request.user)
    return render(request, "cart_list.html", {"items": items})


@login_required(login_url="/users/signin")
def cart_delete(request):
    cart = Cart.objects.get(user = request.user, product = request.product)
    cart.delete()
    return JsonResponse({"message": "상품을 장바구니에서 삭제했습니다."})