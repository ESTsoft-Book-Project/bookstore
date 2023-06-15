from django.shortcuts import render
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from slugify import slugify
from .models import Product
import json

def book_list(request):
    books = Product.objects.all()
    return render(request, 'book_list.html', {'books': books})

def book_detail(request, handle):
    book = get_object_or_404(Product, handle=handle)
    return render(request, 'book_detail.html', {'book': book})

@login_required(login_url="/users/signin/")
def create_product(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        request_data["handle"] = slugify(request_data["name"])
        form = ProductForm(request_data)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({"message": "신규 도서 등록이 완료되었습니다."})
        else:
            return JsonResponse({"message": form.errors.as_json()})
    else:
        return render(request, 'create_product.html')
    
@login_required(login_url="/users/signin/")
def update_product(request, handle):
    book = get_object_or_404(Product, handle=handle)
    context = {"book": book}

    if request.method == "PATCH":
        request_data = json.loads(request.body)
        request_data["handle"] = slugify(request_data["name"])
        form = ProductForm(request_data, instance=book)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return JsonResponse({"message": "도서 정보가 수정되었습니다."}, status = 200)
        else:
            return JsonResponse({"message": form.errors.as_json()}, status = 400)
    if not Product.objects.filter(handle=handle).exists():
        return JsonResponse({"message": "존재하지 않는 상품입니다."}, status = 404)
    else:
        form = ProductForm(instance=book)
        return render(request, "update_product.html", context)